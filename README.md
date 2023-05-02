## Project Description

This project is an API for a restaurant and dish recommendation application. The API is built using Flask and SQLAlchemy, and provides endpoints to get information about restaurants and dishes, as well as to recommend new dishes and restaurants.

The project is fully containerized with Docker, meaning that you can run it without having to worry about any dependencies, as long as you have Docker installed on your system.

## Instructions to Run the Project

Follow these steps to run the application:

1. Clone the repository to your local machine.
2. Open a terminal window and navigate to the project directory.
3. Run `docker-compose up` to start a Docker container running an instance of MariaDB and the Flask application.
4. Once the container is up and running, you can access the application by visiting `http://localhost:5000` in your web browser.

## API Documentation

The API has the following endpoints:

- `/dishes`: returns a list of all dishes in the database.
- `/dishes/<int:id>`: returns a single dish with the provided ID.
- `/restaurants`: returns a list of all restaurants in the database.
- `/restaurants/<int:id>`: returns a single restaurant with the provided ID.
- `/restaurants/<int:id>/dishes`: returns a list of all dishes at the restaurant with the provided ID.
- `/sessions/<int:session_id>/next_dish`: returns the next recommended dish for the provided session.
- `/sessions/<int:session_id>/next_restaurant`: returns the next recommended restaurant for the provided session.
- `/users/<int:user_id>`: returns a single user with the provided ID.
- `/categories`: returns a list of all categories in the database.

To call any of these endpoints, make a GET request to the corresponding URL. The `/sessions/<int:session_id>/next_dish` and `/sessions/<int:session_id>/next_restaurant` endpoints also support automatic session creation if a session ID that does not exist in the database is provided.

The following endpoints also accept POST requests:

- `/users`: creates a new user with a provided username in JSON format. Returns a message with a 201 response status if the user was successfully created.
- `/dishes/<int:dish_id>/like`: adds a "like" to the dish with the provided ID. A username must be provided in JSON format in the request to identify the user who likes the dish. Returns a message with a 200 response status if the like was successfully added.
- `/dishes/<int:dish_id>/comment`: adds a comment to the dish with the provided ID. A username and comment must be provided in JSON format in the request. Returns a message with a 200 response status if the comment was successfully added.

All POST requests must include a `Content-Type` header of `application/json`.