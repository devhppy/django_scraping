import os
from celery import Celery
from celery.schedules import crontab

# Default to a fallback settings module if none is set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devhome.settings")

# Dynamically extract the Django project name from the settings module
settings_module = os.environ["DJANGO_SETTINGS_MODULE"]
project_name = settings_module.split(".")[0]  # e.g., "devhome"

app = Celery(project_name)

# Use Django settings with 'CELERY_' namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks from all registered Django app configs
app.autodiscover_tasks()
