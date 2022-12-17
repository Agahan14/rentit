from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rentit.settings")

app = Celery("rentit")

# finds all rows that have the name celery in settings
app.config_from_object('django.conf:settings', namespace="CELERY")

# so that it automatically finds the task
app.autodiscover_tasks()

# celery beat tasks
app.conf.beat_schedule = {
    'change-status-every-60-minute': {
        'task': 'users.tasks.change_beat_status',
        'schedule': crontab(minute='*/60')
    },
}
