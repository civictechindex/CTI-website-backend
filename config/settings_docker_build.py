import os
# These are the env vars that get retrieved with getenv(). They must be set to avoid raising UnsetEnvironmentVariable.
os.environ['DB_NAME'] = 'fake'
os.environ['DB_USER'] = 'fake'
os.environ['DB_PASSWORD'] = 'fake'
os.environ['DB_HOST'] = 'fake'
os.environ['DB_PORT'] = 'fake'

# noinspection PyUnresolvedReferences
from .settings import *  # noqa F403
