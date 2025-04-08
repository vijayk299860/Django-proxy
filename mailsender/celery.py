# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailsender.settings')

app = Celery('mailsender')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Add periodic task to check for pending emails
app.conf.beat_schedule = {
    'check-pending-emails': {
        'task': 'your_app.tasks.check_pending_emails',
        'schedule': 60.0,  # Every minute
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
