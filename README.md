# Challenge Ed Machina - Backend

Se requiere un proceso de registración de leads a procesar. Lo que se necesita registrar es la persona y las N materias que cursa en N carreras.

## Instalación
Para correr el proyecto, sobre el directorio se deben correr los siguientes comandos:

```shell
> docker-compose build

> docker-compose up
```

Los endpoints de la API y esquemas asociados se encontrarán en la url [localhost:8000/docs](http://localhost:8000/docs).

## Uso

La API cuenta con tres endpoints, `/degrees`, `/students`, y `/leads`: 

---

#### `POST` `/degrees`
*Inserta una carrera en la base de datos, en base a la información introducida en el body, y devuelve la carrera guardada junto con su `id`.*

Los datos a ingresar por carrera son:

| Nombre        | Descripción                       | Tipo     |
| :------------ |:----------------------------------|:---------|
| name          | Nombre de la carrera              | `string` |
| length_years  | Duración de la carrera en años    |  `int`   |

---

#### `GET` `/degrees`
*Devuelve todas las carreras registradas en la base de datos.*

La respuesta es una lista de `Degrees`, en donde el formato de cada item es:
| Nombre        | Descripción                       | Tipo     |
| :------------ |:----------------------------------|:---------|
| name          | Nombre de la carrera              | `string` |
| length_years  | Duración de la carrera en años    |  `int`   |
| id            | Identificador único de la carrera |  `int`   |

Ejemplo de respuesta:
```python
[
  {
    "name": "Ingeniería en Sistemas",
    "length_years": 5,
    "id": 1
  },
  {
    "name": "Ingeniería Electrónica",
    "length_years": 5,
    "id": 2
  }
]
```

---

#### `POST` `/subjects`
*Inserta una materia en la base de datos, en base a la información introducida en el body, y devuelve la materia guardada junto con su `id`.*

Los datos a ingresar por materia son:

| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| name          | Nombre de la materia                  | `string` |
| total_hours   | Duración de la materia en horas       |  `int`   |
| degree_id     | Id de la carrera a la que pertenece   |  `int`   |


---

#### `GET` `/subjects`
*Devuelve todas las materias registradas en la base de datos.*

La respuesta es una lista de `Subjects`, en donde el formato de cada item es:
| Nombre        | Descripción                       | Tipo     |
| :------------ |:----------------------------------|:---------|
| name          | Nombre de la materia              | `string` |
| total_hours   | Duración de la materia en horas   |  `int`   |
| degree        | Carrera a la que pertenece        | `Degree` |

Ejemplo de respuesta:
```python
[
  {
    "name": "Estructuras de Datos",
    "total_hours": 128,
    "id": 1,
    "degree": {
      "name": "Ingeniería en Sistemas",
      "length_years": 5,
      "id": 1
    }
  },
  {
    "name": "Principios de Computadoras II",
    "total_hours": 112,
    "id": 2,
    "degree": {
      "name": "Ingeniería Electrónica",
      "length_years": 5,
      "id": 2
    }
  }
]
```

---


#### `POST` `/leads`
*Inserta un lead en la base de datos, en base a la información introducida en el body. Devuelve el `Lead` guardado junto con su `id` de registro.*

El lead consiste en datos de un estudiante, la lista de carreras en las que está inscripto, y la lista de materias en las que está anotado.

Los datos a ingresar por lead son:

| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| name          | Nombre del estudiante                 | `string` |
| email   | Email del estudiante       |  `string`   |
| address     | Dirección del estudiante   |  `string`   |
| phone     | Teléfono del estudiante   |  `int`   |
| degrees     | Lista de carreras del estudiante   |  `list[StudentDegreeCreate]`   |
| subjects     | Lista de materias del estudiante   |  `list[StudentSubjectCreate]`   |

Los últimos dos campos corresponden a asociaciones entre estudiante y carreras/materias respectivamente. Los formatos de estos dos objetos son los siguientes:

`StudentDegreeCreate`:
| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| degree_id          | Id de la carrera          | `int` |
| enrollment_year   | Año de inscripción       |  `int`   |

`StudentSubjectCreate`:
| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| subject_id          | Id de la materia          | `int` |
| attempt_number   | Número de intento       |  `int`   |


Ejemplo de datos para registrar un lead:
```python
{
  "name": "Ramiro Suriano",
  "email": "rs@uns.edu.ar",
  "address": "Alem 1400",
  "phone": 1123581321,
  "degrees": [
    {
      "degree_id": 2
      "enrollment_year": 2014,
    }
  ],
  "subjects": [
    {
      "attempt_number": 1,
      "subject_id": 2
    },
    {
      "attempt_number": 2,
      "subject_id": 4
    },
  ]
}
```

---

#### `GET` `/leads`
*Devuelve todos los leads registrados en la base de datos, paginados en base a los parámetros de la request:*

| Parámetro        | Descripción                       | Tipo     | Valor predeterminado |
| :------------ |:----------------------------------|:---------|:---------|
| skip          | Saltea esta cantidad de resultados      | `int` | 0 |
| limit   | Cantidad máxima de objetos a devolver   |  `int`   | 10 |

El formato de respuesta es una lista de `Leads`, en donde cada lead tiene el siguiente formato:
| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| name          | Nombre del estudiante                 | `string` |
| email   | Email del estudiante       |  `string`   |
| address     | Dirección del estudiante   |  `string`   |
| phone     | Teléfono del estudiante   |  `int`   |
| degrees     | Lista de carreras del estudiante   |  `list[StudentDegree]`   |
| subjects     | Lista de materias del estudiante   |  `list[StudentSubject]`   |

En este caso, los formatos de los últimos dos campos son los siguientes:

`StudentDegree`:
| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| degree          | Carrera asociada          | `Degree` |
| enrollment_year   | Año de inscripción       |  `int`   |

`StudentSubject`:
| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| subject          | Materia asociada          | `Subject` |
| attempt_number   | Número de intento       |  `int`   |

Ejemplo de respuesta:
```python
[
  {
    "name": "Ramiro Suriano",
    "email": "rs@uns.edu.ar",
    "address": "Alem 1400",
    "phone": 1123581321,
    "id": 1,
    "degrees": [
      {
        "enrollment_year": 2014,
        "degree": {
          "name": "Ingeniería Electrónica",
          "length_years": 5,
          "id": 2
        }
      }
    ],
    "subjects": [
      {
        "attempt_number": 1,
        "subject": {
          "name": "Principios de Computadoras II",
          "total_hours": 112,
          "id": 2,
          "degree": {
            "name": "Ingeniería Electrónica",
            "length_years": 5,
            "id": 2
          }
        }
      },
      {
        "attempt_number": 2,
        "subject": {
          "name": "Fundamentos de Control Realimentado",
          "total_hours": 128,
          "id": 4,
          "degree": {
            "name": "Ingeniería Electrónica",
            "length_years": 5,
            "id": 2
          }
        }
      }
    ]
  },
  {
    "name": "Juan Rodriguez",
    "email": "jr@uns.edu.ar",
    "address": "Alem 1400",
    "phone": 314159265,
    "id": 2,
    "degrees": [
      {
        "enrollment_year": 2018,
        "degree": {
          "name": "Ingeniería en Sistemas",
          "length_years": 5,
          "id": 1
        }
      }
    ],
    "subjects": [
      {
        "attempt_number": 1,
        "subject": {
          "name": "Estructuras de Datos",
          "total_hours": 128,
          "id": 1,
          "degree": {
            "name": "Ingeniería en Sistemas",
            "length_years": 5,
            "id": 1
          }
        }
      }
    ]
  }
]
```


#### `GET` `/leads/{lead_id}`
*Devuelve el lead con numero de registro correspondiente al parámetro `lead_id`.*

El formato de respuesta es un objeto `Lead`, con el mismo formato que en la sección anterior, que se repite por conveniencia:
| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| name          | Nombre del estudiante                 | `string` |
| email   | Email del estudiante       |  `string`   |
| address     | Dirección del estudiante   |  `string`   |
| phone     | Teléfono del estudiante   |  `int`   |
| degrees     | Lista de carreras del estudiante   |  `list[StudentDegree]`   |
| subjects     | Lista de materias del estudiante   |  `list[StudentSubject]`   |

Al igual que los formatos de los últimos dos campos:

`StudentDegree`:
| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| degree          | Carrera asociada          | `Degree` |
| enrollment_year   | Año de inscripción       |  `int`   |

`StudentSubject`:
| Nombre        | Descripción                           | Tipo     |
| :------------ |:--------------------------------------|:---------|
| subject          | Materia asociada          | `Subject` |
| attempt_number   | Número de intento       |  `int`   |

Ejemplo de respuesta, con `{lead_id} = 1`:
```python
[
  {
    "name": "Ramiro Suriano",
    "email": "rs@uns.edu.ar",
    "address": "Alem 1400",
    "phone": 1123581321,
    "id": 1,
    "degrees": [
      {
        "enrollment_year": 2014,
        "degree": {
          "name": "Ingeniería Electrónica",
          "length_years": 5,
          "id": 2
        }
      }
    ],
    "subjects": [
      {
        "attempt_number": 1,
        "subject": {
          "name": "Principios de Computadoras II",
          "total_hours": 112,
          "id": 2,
          "degree": {
            "name": "Ingeniería Electrónica",
            "length_years": 5,
            "id": 2
          }
        }
      },
      {
        "attempt_number": 2,
        "subject": {
          "name": "Fundamentos de Control Realimentado",
          "total_hours": 128,
          "id": 4,
          "degree": {
            "name": "Ingeniería Electrónica",
            "length_years": 5,
            "id": 2
          }
        }
      }
    ]
  }
]
```

