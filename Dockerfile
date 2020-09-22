  
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential procps \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev libpq5 postgresql-client \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# create root directory for our project in the container
RUN mkdir /code

# Set the working directory to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/
EXPOSE 8000
CMD python3 manage.py runserver 0.0.0.0:8000
