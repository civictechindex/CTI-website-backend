# CTI-Website-Backend
## Running Locally 

- Import data from data source
    - [Excel Sheet](https://drive.google.com/file/d/1xiLeyMwZc-n6eB1R_XdCJ00YrarfnR_w/view)
    - Download as csv
    - Upload the csv file in the project root 

Below are the steps to get started using docker and pip

- Create a .env file inside /config for writing the database credentials, example below
```
POSTGRES_NAME='postgres'
POSTGRES_PASSWORD='postgres'
POSTGRES_USER='postgres'
POSTGRES_HOST='db'
```

### Getting Started with Docker

- Steps to setup the Django Administration Page

- Execute the docker-compose steps
```
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py import_initial_data filename.csv
```

### Getting Started with pip

- Create and activate a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- Install the packages
``pip install -r requirements.txt``

- Execute the following steps
```
python manage.py migrate
python manage.py createsuperuser
python manage.py import_initial_data filename.csv
python manage.py runserver
```

### After succesful execution of either of the above two steps -> Docker or pip 
- Navigate to the Django Administration Page http://127.0.0.1:8000/admin/
- Login using superuser credentials
