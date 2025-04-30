# import os
# from celery import Celery
# from celery.schedules import crontab

# # Default to a fallback settings module if none is set
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devhome.settings")

# # Dynamically extract the Django project name from the settings module
# settings_module = os.environ["DJANGO_SETTINGS_MODULE"]
# project_name = settings_module.split(".")[0]  # e.g., "devhome"



# app = Celery(project_name)

# # Use Django settings with 'CELERY_' namespace
# app.config_from_object("django.conf:settings", namespace="CELERY")

# # Autodiscover tasks from all registered Django app configs
# app.autodiscover_tasks()


# # from helpers.cassi import sync_all_tables
# # sync_all_tables()

from __future__ import absolute_import, unicode_literals
import os

# 1. Point to Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devhome.settings")

# 2. Bootstrap Django
import django
django.setup()

# 3. Initialize Cassandra (only once per process)
from helpers.cassi import get_session, sync_all_tables
get_session()
sync_all_tables()

# 4. Create and configure Celery
from celery import Celery
app = Celery("devhome")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
