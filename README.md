# CTI-Website-Backend
[![Maintainability](https://api.codeclimate.com/v1/badges/8051528982d28405e1bb/maintainability)](https://codeclimate.com/github/civictechindex/CTI-website-backend/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8051528982d28405e1bb/test_coverage)](https://codeclimate.com/github/civictechindex/CTI-website-backend/test_coverage)

## Contributing

If you would like to contribute to the Civic Tech Index project, please see the
issues and project management board in the [repository for the React
app](https://github.com/civictechindex/CTI-website-frontend/) which uses this
Django app as its API backend.

This project uses Django with Django REST Framework. If you are not already
familiar with Django, we suggest you work through the [Django
tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/) and the
[Django REST Framework
tutorial](https://www.django-rest-framework.org/tutorial/quickstart/) to get
familiar with the tools this project uses. (Don't spend too long on these; just
use them to get a feel for Django development.)

This project can be run using Docker OR installed directly on your machine.


### Running this project on your machine with Docker

This repository contains a Dockerfile for building a container for running our
Django project - in dev and in AWS via FARGATE. To use Docker for development,
you will want to use the project's `docker-compose.yaml` to also create a
Postgres database container, a volume for persisting your data, and a network
that allows your web container to talk to your database container.

1. Install Docker
2. Clone this repository
3. Copy `config/.env.example` to `config/.env`
4. Build and configure your docker container by running the following command:
    ```
    docker-compose up -d --build
    ```
5. Our `docker-compose.yaml` creates a volume for persisting the database
   information so you should only have to run the migrations, load the data, and
   create a superuser the first time you create your containers.
    ```
    init/setup-db.sh
    ```

### Running this project directly on your machine (no containers)

1. Install [PostgreSQL](https://www.postgresql.org/) if you haven't already.
2. Clone this repository
3. Create and activate a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
4. Install the packages
    ```
    pip install -r requirements.txt
    ```
5. Copy `config/.env.example` to `config/.env` and edit to provide the database
   credentials your project will use. The contents of your .env file should
   provide the following information (though the values for user, host, db will
   depend on how you have configured your local Postgres database):
    ```
    POSTGRES_NAME='postgres'
    POSTGRES_PASSWORD='postgres'
    POSTGRES_USER='postgres'
    POSTGRES_HOST='localhost'
    ```
6. Execute the following steps to load the environment variables from above and
   set up your database. You should only need to do these steps the first time
   you create a new database.
    ```
    source config/.env
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py loaddata init/organizations.json
    ```
7. Start your web server in the foreground:
    ```
    source config/.env
    python manage.py runserver
    ```


### Using this project to manage your data
- Navigate to the Django Administration Page http://127.0.0.1:8888/admin/
- Login using superuser credentials
- This takes you to the Django admin interface for this project

### To run the automated tests in this project

If you are running this project using Docker, log into the docker container: `docker exec -ti cti-web /bin/bash`

From the root of the project, run the tests: `pytest`

To run tests and see the coverage report run: `pytest --cov=civictechindexadmin`
