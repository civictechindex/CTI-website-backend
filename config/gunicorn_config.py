import environ

env = environ.Env()

# general
bind = 'unix:/tmp/cti-web.sock'
workers = 8
worker_class = 'sync'
daemon = False
timeout = 300
worker_tmp_dir = '/tmp'

# requires futures module for threads > 1
threads = 1

# During development, this will cause the server to reload when the code changes.
reload = env.bool('GUNICORN_RELOAD', default=False)

# Logging.
accesslog = '-'
access_log_format = '%({X-Forwarded-For}i)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
errorlog = '-'
syslog = False

