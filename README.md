## Descripción del Proyecto

Este proyecto es una API para una aplicación de recomendación de restaurantes y platos de comida. La API se construyó utilizando Flask y SQLAlchemy, y proporciona endpoints para obtener información sobre restaurantes y platos, así como para recomendar nuevos platos y restaurantes.

## Instrucciones para ejecutar el proyecto

Siga estos pasos para ejecutar la aplicación:

1. Cree un entorno virtual con `virtualenv env`.
2. Active el entorno virtual con `source env/bin/activate`.
3. Instale las dependencias del proyecto con `pip install -r requirements.txt`.
4. Ejecute la aplicación con `python app.py`.

## Documentación de la API

La API tiene los siguientes endpoints:

- `/dishes`: devuelve una lista de todos los platos en la base de datos.
- `/dishes/<int:id>`: devuelve un solo plato con el ID proporcionado.
- `/restaurants`: devuelve una lista de todos los restaurantes en la base de datos.
- `/restaurants/<int:id>`: devuelve un solo restaurante con el ID proporcionado.
- `/restaurants/<int:id>/dishes`: devuelve una lista de todos los platos en el restaurante con el ID proporcionado.
- `/sessions/<int:session_id>/next_dish`: devuelve el siguiente plato recomendado para la sesión proporcionada.
- `/sessions/<int:session_id>/next_restaurant`: devuelve el siguiente restaurante recomendado para la sesión proporcionada.

Para llamar a cualquiera de estos endpoints, haga una solicitud GET a la URL correspondiente. Los endpoints `/sessions/<int:session_id>/next_dish` y `/sessions/<int:session_id>/next_restaurant` también admiten creación automática de sesión si se proporciona un ID de sesión que no existe en la base de datos.