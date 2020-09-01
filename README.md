# CTI-Website-Backend
## Running Locally 

- Import data from data source
    - [Excel Sheet] (https://drive.google.com/file/d/1xiLeyMwZc-n6eB1R_XdCJ00YrarfnR_w/view)
    - Download as csv
    - Upload the csv file in the project root 

Below are the steps to get started using docker and pip

### Getting Started with Docker

- Initialise the Django Administration Page
- Go to manage.py file and verify the settings file is pointing correctly
    - ``os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.docker_settings") ``
```
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py import_initial_data filename.csv
```

### Getting Started with pip

- Create and activate a [virtual environment] (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- Install the packages
``pip install -r requirements.txt``
- Go to manage.py file and verify the settings file is pointing correctly
    - ``os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.local_settings") ``
- Create a Database with the following credentails 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'civictechindexadmin',
        'USER': 'civictechindexroot',
        'PASSWORD': 'civictechindexroot',
        'HOST': 'localhost',
        'PORT': 5432
    }
}
```

- Execute the following steps
```
python manage.py migrate
python manage.py createsuperuser
python manage.py import_initial_data filename.csv
python manage.py runserver
```

- After succesful execution of either of the above two steps -> Docker or pip 
    - Navigate to the Django Administration Page http://127.0.0.1:8000/admin/
    - Login using in superuser credentials
