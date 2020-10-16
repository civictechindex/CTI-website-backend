import os
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username=os.environ.get('SU_USERNAME')).exists():
    User.objects.create_superuser(os.environ.get('SU_USERNAME'),
                                  os.environ.get('SU_EMAIL'),
                                  os.environ.get('SU_PASSWORD')
                                  )
