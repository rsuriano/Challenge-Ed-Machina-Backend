## Documentación Tecnica
---

## Scripts backend
Esta aplicación cuenta con 5 scripts que están separados por distintos scopes:

1. `db_conn`, en donde se configura la conexión mediante `SQL Alchemy` con la base de datos.
2. `models`, en donde se definen las entidades y relaciones necesarias para el guardado de los leads.
3. `schemas`, en donde se definen mediante `Pydantic` los esquemas para creación y obtención de datos.
4. `crud`, en donde se definen las funciones para crear y recibir elementos de la base de datos.
5. `api`, en donde se definen los endpoints y las funciones que ejecuta cada request, por medio de `FastAPI`.

---

### 1. `db_conn` | **Conexión con base de datos:**
Este módulo inicializa la conexión con la base de datos utilizando la librería `SQL Alchemy`.

Utiliza el string de conexión correspondiente a la base de datos de Postgres que se encuentra definida como servicio en el archivo `docker-compose.yml`, en la carpeta root del repositorio.

Finalmente crea las variables `engine`, `SessionLocal` y `Base`, para interactuar con la base de datos y definir los modelos necesarios.

---

### 2. `models` | **Entidades y relaciones:**
En este módulo se definen las clases principales de la aplicación:
- `Degree`: representa una carrera universitaria que tiene materias en su plan y estudiantes inscriptos a ella.
- `Subject`: representa una materia que pertenece a una carrera, y que tiene estudiantes inscriptos. 
- `Student`: representa un estudiante que tiene carreras y materias a las que está inscripto. Esta clase es la llamada `Lead` en las capas superiores de la aplicación.

En cuanto a las relaciones, se optó por definir relaciones de muchos a muchos entre los tres elementos, para dar robustez a los datos introducidos en el sistema. 

De esta forma, al cargar carreras, materias y "leads" (que internamente son estudiantes), se generan automáticamente las asociaciones que permiten obtener a futuro (y con agregados mínimos de código) información adicional como la lista de estudiantes inscriptos a una materia o carrera, o el plan de materias de cada carrera.

La única relación de uno a muchos se encuentra entre `Degree` y `Subject`, esto en principio se implementó de esta forma para no complejizar de más el sistema, si bien se reconoce que en la vida real pueden haber materias que pertenezcan a varias carreras, por ejemplo si la universidad mantiene un sistema de Departamentos en lugar de Facultades.

Para crear el resto de las relaciones se definieron dos [Association Objects](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object), ya que al haber datos adicionales para cada asociación (el año de inscripción para la tabla `StudentDegree`, y el número de intentos para la tabla `StudentSubject`) no es suficiente con una [Association Table](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many).

Finalmente, todas las relaciones fueron definidas bidireccionalmente utilizando `back_populates`, para poder actualizar las relaciones desde cualquiera de los dos extremos.

---

### 3. `schemas` | **Modelos de Pydantic:**
En este módulo se definen modelos o esquemas para utilizar como plantillas para guardado y obtención de datos, así como tambien los tipos de cada campo para que `FastAPI` realice la validación al momento de recibirse una request.

Como resumen, en las clases con sufijo `Base` se agregan los campos básicos de cada modelo, mientras que en las clases con sufijo `Create` (que heredan los campos de `Base`), se agregan los campos necesarios para cargar las relaciones con las otras tablas. Finalmente, en las clases sin sufijo (que tambien heredan de `Base`) se agregan los campos que obtiene el usuario al recibir objetos de la api.

De esta forma, para agregar por ejemplo un `Degree` solo necesitamos los campos `name` y `total_years`, pero al recibir luego este objecto `Degree` de la base de datos tenemos ademas de estos dos el campo `id` que antes no existía.

Por ejemplo, para la clase `Degree`:

```python
# DegreeCreate
{
    name: str
    total_years: int
}

# Degree
{
    name: str
    total_years: int
    id: int
}
```

#### **CustomGetters**
Estos esquemas adicionales son necesarios para poder mostrar tanto la lista de carreras como de materias de un estudiante. 

Cuando Pydantic genera una respuesta utilizando el esquema `Student`, intenta acceder a los campos de `Degree` y `Subject` dentro de `StudentDegree` y `StudentSubject`, pero estos objetos se encuentran un nivel mas abajo. Para evitar este error, se agrega un *Custom Getter Dict*, que le dice a Pydantic que acceda primero al objeto `Degree` dentro de `StudentDegree` y luego si acceda a los campos de `Degree` (y lo mismo para `Subject` dentro de `StudentSubject`).

---

### 4. `crud` | **Interacción con base de datos:**
En este módulo se definen las funciones que se utilizarán para crear y obtener elementos de la base de datos.

Las funciones de `update` y `delete` se omitieron por considerarse fuera del scope del challenge.

**Creación de datos**
- `create_degree`: Crea un objeto `Degree` y lo agrega a la base de datos. Tiene también protección contra agregado de degrees duplicados (por campo `name`), en este caso genera una excepción HTTP con código 400 (bad request).
- `create_subject`: Chequea si el `Degree` asociado a la materia es existente, si no lo es genera una excepcion HTTP con código 400. Si el `Degree` existe, crea un objeto `Subject` y su relación con `Degree`, y lo guarda en base de datos. Al igual que `Degree`, cuenta con protección contra guardado de datos duplicados (por campo `name`).
- `create_lead`: Crea un Lead, que consiste en un objeto `Student` con su lista de `Degrees` y `Subjects` asociados. Cuenta con protecciones contra registros duplicados de estudiante (por campo `email`), inscripciones a carreras, e inscripciones a materias. Tambien detecta carreras y materias inexistentes en base de datos, así como también si se intenta agregar una materia que pertenece a una carrera a la que el estudiante no está inscripto. Todos estos errores devuelven una HTTPException con código 400, y mensajes de error describiendo el problema hallado.

**Obtención de datos**
- `get_degree_by_id`: Obtiene un solo `Degree` a partir de su `id`.
- `get_degree`: Obtiene todos los `Degrees` disponibles.
- `get_subject_by_id`: Obtiene un solo `Subject` a partir de su `id`.
- `get_subjects`: Obtiene todos los `Subjects` disponibles.
- `get_student_by_email`: Obtiene un `Student` a partir de su `id`. Esta función se utiliza para chequear duplicados a la hora de procesar un nuevo Lead, ya que el campo `email` es único.
- `get_student_by_id`: Obtiene un `Student` a partir de su `id`. En esta función y la siguiente se añadieron opciones de `JoinedLoad` para que SQL Alchemy obtenga de base de datos también los objetos a los que apuntan las relaciones `Student.degrees` y `Student.subjects`.
- `get_students`: Obtiene los `Students` en base a los parámetros `skip` y `limit`, logrando asi que se obtengan los datos paginados.

---

### 5. `api` | **Definición de endpoints:**
En este módulo se definen los tres endpoints principales explicados en la [documentación funcional](https://github.com/rsuriano/Challenge-Ed-Machina-Backend/blob/develop/README.md).

Además se crean las tablas correspondientes a los modelos definidos en `models`, y se agrega metadata a la documentación de FastAPI.

Por otro lado, se crea una dependencia que obtiene una sesión de base de datos, la utiliza para realizar la transacción necesaria, y finalmente cierra la sesión. De esta forma no se mantiene abierta la sesión todo el tiempo, y solo está activa cuando se accede a algún endpoint.

A continuación se definen los endpoints, asociandoles un esquema de los definidos en `schemas`, y llamando dentro de cada función las operaciones definidas en `crud`.


---
&nbsp;

## Docker
Para poder correr la app en cualquier sistema, se creó un `Dockerfile` en el directorio `backend`, en donde se define la versión de Python, se instalan las librerías necesarias, y se copian los archivos descriptos anteriormente. Finalmente se ejecuta el comando de `uvicorn` que corre la api en el puerto 8000.

Además hay un script adicional, `data_loader`, dentro del directorio `data_load`, que carga datos a la base de datos para poder probar endpoints sin tener que agregar datos previamente.

En el directorio principal del repositorio se creó un archivo `docker-compose`, el cual levanta tres contenedores:
1. Uno propio que contiene todo el código del backend (cuya imagen se construye a partir del `Dockerfile` definido anteriormente).
2. El servicio `data_load`, que agrega datos de muestra a la base de datos.
3. Una imagen oficial de Postgres que provee de persistencia al sistema. También se define un volumen para que los datos de Postgres no se pierdan al borrar el contenedor.

Por último se mapean los puertos internos de los contenedores a los de la computadora, para poder acceder de forma externa a los servicios.

---
&nbsp;

## Definición lead-student
En varios lugares se usa la palabra Lead y la palabra Student para referirse al mismo objeto. Esto es porque se considera un Lead a un dato externo que se carga mediante la API. Una vez dentro del sistema, la información del Lead se mapea a nuestra clase `Student`. 
En otras palabras, se considera que el Lead es información que popula al objeto `Student`.


