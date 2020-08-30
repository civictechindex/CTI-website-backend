  
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start
COPY --chown=django:django . /app

USER django

#FROM garland/aws-cli-docker:1.15.47

#COPY ./compose/production/aws/maintenance /usr/local/bin/maintenance
#COPY ./compose/production/postgres/maintenance/_sourced /usr/local/bin/maintenance/_sourced

#RUN chmod +x /usr/local/bin/maintenance/*

#RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
#    && rmdir /usr/local/bin/maintenance



  
#FROM traefik:v2.0
#RUN mkdir -p /etc/traefik/acme
#RUN touch /etc/traefik/acme/acme.json
#RUN chmod 600 /etc/traefik/acme/acme.json
#COPY ./compose/production/traefik/traefik.yml /etc/traefik

EXPOSE 8000
CMD exec gunicorn config.wsgi:application — bind 0.0.0.0:8000 — workers 3
WORKDIR /app

ENTRYPOINT ["python","manage.py"]
