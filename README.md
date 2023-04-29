## Descripción del Proyecto

Este proyecto es una API para una aplicación de recomendación de restaurantes y platos de comida. La API se construyó utilizando Flask y SQLAlchemy, y proporciona endpoints para obtener información sobre restaurantes y platos, así como para recomendar nuevos platos y restaurantes.

## Instrucciones para ejecutar el proyecto

Siga estos pasos para ejecutar la aplicación:

1. Cree un entorno virtual con `virtualenv env`.
2. Active el entorno virtual con `source env/bin/activate`.
3. Instale las dependencias del proyecto con `pip install -r requirements.txt`.
4. Ejecute la aplicación con `flask run`.

A continuación, se proporciona una instrucción adicional para levantar la base de datos necesaria para la aplicación utilizando `docker-compose`.

## Levantar la base de datos con Docker Compose

1. Asegúrese de tener instalado Docker Compose en su sistema.
2. Abra una terminal en la raíz del proyecto.
3. Ejecute `docker-compose up` para iniciar un contenedor de Docker que ejecute una instancia de PostgreSQL.
4. Una vez que el contenedor esté en ejecución, puede ejecutar la aplicación utilizando las instrucciones proporcionadas en la sección "Instrucciones para ejecutar el proyecto". 

Es importante destacar que `docker-compose` leerá el archivo `docker-compose.yaml` ubicado en la raíz del proyecto para crear y configurar el contenedor de la base de datos. Asegúrese de que la información de la base de datos en `app/config.py` coincida con la configuración de `docker-compose.yml`.

## Documentación de la API

La API tiene los siguientes endpoints:

- `/dishes`: devuelve una lista de todos los platos en la base de datos.
- `/dishes/<int:id>`: devuelve un solo plato con el ID proporcionado.
- `/dishes/<int:dish_id>/like`: agrega un "me gusta" al plato con el ID proporcionado.
- `/dishes/<int:dish_id>/comment`: agrega un comentario al plato con el ID proporcionado.
- `/restaurants`: devuelve una lista de todos los restaurantes en la base de datos.
- `/restaurants/<int:id>`: devuelve un solo restaurante con el ID proporcionado.
- `/restaurants/<int:id>/dishes`: devuelve una lista de todos los platos en el restaurante con el ID proporcionado.
- `/sessions/<int:session_id>/next_dish`: devuelve el siguiente plato recomendado para la sesión proporcionada.
- `/sessions/<int:session_id>/next_restaurant`: devuelve el siguiente restaurante recomendado para la sesión proporcionada.
- `/users`: crea un nuevo usuario.
- `/users/<int:user_id>`: devuelve un solo usuario con el ID proporcionado.
- `/categories`: devuelve una lista de todas las categorías en la base de datos.

Para llamar a cualquiera de estos endpoints, haga una solicitud GET a la URL correspondiente. Los endpoints `/sessions/<int:session_id>/next_dish` y `/sessions/<int:session_id>/next_restaurant` también admiten creación automática de sesión si se proporciona un ID de sesión que no existe en la base de datos.

Los siguientes endpoints también aceptan solicitudes POST:

- `/users`: crea un nuevo usuario con un nombre de usuario proporcionado en formato JSON. Retorna un mensaje con un estado de respuesta 201 si se creó exitosamente el usuario.
- `/dishes/<int:dish_id>/like`: agrega un "me gusta" al plato con el ID proporcionado. Se debe proporcionar un nombre de usuario en formato JSON en la solicitud para identificar al usuario que le gusta el plato. Retorna un mensaje con un estado de respuesta 200 si se agregó el "me gusta" exitosamente y un estado de respuesta 400 si el plato ya tiene un "me gusta" de ese usuario.
- `/dishes/<int:dish_id>/comment`: agrega un comentario al plato con el ID proporcionado. Se debe proporcionar un nombre de usuario y un comentario en formato JSON en la solicitud. Retorna un mensaje con un estado de respuesta 200 si se agregó el comentario exitosamente. 

Todas las solicitudes POST deben incluir un encabezado de tipo de contenido `application/json`.