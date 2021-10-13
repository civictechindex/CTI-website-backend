FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
# Disable writing .pyc files - but only during docker build
ARG PYTHONDONTWRITEBYTECODE=1

RUN apt-get update -y && \
    apt-get install -y gnupg2 wget && \
    wget --quiet -O /tmp/pg-repo.asc https://www.postgresql.org/media/keys/ACCC4CF8.asc && \
    apt-key add /tmp/pg-repo.asc && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" >  /etc/apt/sources.list.d/pgdg.list && \
    apt-get update -y && \
    apt-get install -y libenchant-dev libpq-dev postgresql-client-12 && \
    # dependencies for building Python packages
    apt-get install -y build-essential procps && \
    # Translations dependencies
    apt-get install -y gettext && \
    # Nginx web server
    apt-get install -y nginx-light && \
    # cleaning up unused files
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

    # Install supervisor globally
RUN pip install supervisor && \
    # Create the venv for votes's environment to live it.
    python -m venv /ve && \
    # Add the user under which gunicorn will run.
    adduser gunicorn && \
    # Add the user under which nginx will run.
    adduser nginx && \
    # Set the container's timezone to Los Angeles time.
    rm -rf /etc/localtime && \
    ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

# Ensure that we run the pip and python that are in the virtualenv, rather than the system copies.
ENV PATH /ve/bin:$PATH

# Install the latest pip and our dependencies into the virtualenv.  We do this before copying the codebase so that minor
# code changes don't force a rebuild of the entire virtualenv.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Copy the code into the image. The .dockerignore file determines what gets left out of this operation. This step will
# always invalidate the docker build cache, so it's done as late as possible to make sure the fewest number of steps
# must be repeated on each build of the image.
COPY . /code
WORKDIR /code

# Copy/create/delete various config files and folders.
RUN cp etc/supervisord.conf /etc/supervisord.conf && \
    cp etc/nginx.conf /etc/nginx/nginx.conf && \
    cp etc/gunicorn_logging.conf /etc/gunicorn_logging.conf && \
    pip3 install -e . && \
    # Run collectstatic to symlink all the static files into /static, which is where the webserver expects them.
    mkdir /static && \
    python manage.py collectstatic --settings=config.settings_docker_build --noinput -v0 --link && \
    chown -R nginx:nginx /static

EXPOSE 8000

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
