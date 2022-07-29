# Challenge Ed Machina - Backend
## Documentación Tecnica
---

### Scripts backend
Esta aplicación cuenta con 5 scripts que están separados por distintos scopes:

1. `db_conn`, en donde se configura la conexión mediante `SQL Alchemy` con la base de datos.
2. `models`, en donde se definen las entidades y relaciones necesarias para el guardado de los leads.
3. `schemas`, en donde se definen mediante `Pydantic` los esquemas para creación y obtención de datos.
4. `crud`, en donde se definen las funciones para crear y recibir elementos de la base de datos.
5. `api`, en donde se definen los endpoints y las funciones que ejecuta cada request, por medio de `FastAPI`.

---

### 1- `db_conn`:
Este primer módulo inicializa la conexión con la base de datos utilizando la librería `SQL Alchemy`.

Utiliza el string de conexión correspondiente a la base de datos de Postgres que se encuentra definida como servicio en el archivo `docker-compose.yml`, en la carpeta root del repositorio.

