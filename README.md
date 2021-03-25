# CTI-Website-Backend
[![Maintainability](https://api.codeclimate.com/v1/badges/8051528982d28405e1bb/maintainability)](https://codeclimate.com/github/civictechindex/CTI-website-backend/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8051528982d28405e1bb/test_coverage)](https://codeclimate.com/github/civictechindex/CTI-website-backend/test_coverage)

## Contributing

If you would like to contribute to the Civic Tech Index project, please go to the [repository for the
React app](https://github.com/civictechindex/CTI-website-frontend/) which uses this Django app as it's API backend.

This project uses Django with Django REST Framework. If you are not already familiar with Django, we suggest
you work through the [Django tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/) and the [Django
REST Framework tutorial](https://www.django-rest-framework.org/tutorial/quickstart/) to get familiar with the
tools this project uses. (Don't spend too long on these; just use them to get a feel for Django development.)

### Getting started with either method below

1. Clone this repository
2. Get a copy of the initial data:
    - [Excel Sheet](https://drive.google.com/file/d/1xiLeyMwZc-n6eB1R_XdCJ00YrarfnR_w/view)
    - Download as csv to the project root. Make sure you choose the `CSV (Comma delimited) (*.csv)` option. In the steps below we refer to this file as `filename.csv`
3. Install [PostgreSQL](https://www.postgresql.org/) if you haven't already.



#### Running this project on your machine with Docker

1. Install Docker
3. Create a .env file inside the `config` subdirectory. This .env file contains the the database credentials
   your project will use. The contents of your .env file should be the following:

    ```
    POSTGRES_NAME='postgres'
    POSTGRES_PASSWORD='postgres'
    POSTGRES_USER='postgres'
    POSTGRES_HOST='db'
    ```

4. Build and configure your docker container by running the following commands. Our `docker-compose.yaml` creates
   a volume for persisting the database information so you will need to do the first step below each time you start
   working on this code but you should only have to run the migrations and load data the first time you create your containers.

    ```
    docker-compose up -d --build
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py import_initial_data filename.csv
    ```

#### Running this project directly on your machine (no containers)

1. Create and activate a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
2. Install the packages
``pip install -r requirements.txt``
3. Create a .env file inside the `config` subdirectory. This .env file contains the the database credentials
   your project will use. The contents of your .env file should be the following:

    ```
    POSTGRES_NAME='postgres'
    POSTGRES_PASSWORD='postgres'
    POSTGRES_USER='postgres'
    POSTGRES_HOST='localhost'
    ```
4. Execute the following steps

    ```
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py import_initial_data filename.csv
    python manage.py runserver
    ```

### Using this project to manage your data
- Navigate to the Django Administration Page http://127.0.0.1:8888/admin/
- Login using superuser credentials
- This takes you to the Django admin interface for this project

### To run the automated tests in this project

1. Log into the docker container: `docker exec -ti cti-website-backend_web_1 /bin/bash`
2. Run tests: `pytest`
3. To run tests and see the coverage report run: `pytest --cov=civictechindexadmin`
