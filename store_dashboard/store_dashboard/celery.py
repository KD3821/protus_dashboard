import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
BROKER_HOST = os.getenv("BROKER_HOST")
report_time = os.getenv("REPORT_TIME")

if report_time is None:
    report_time = "21:00"

report_hours, report_minutes = report_time.split(":")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store_dashboard.settings")
app = Celery("store_dashboard")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = f"redis://{BROKER_HOST}:6379/0"
app.conf.result_backend = f"mongodb://{DB_HOST}:27017/{DB_NAME}"
app.conf.beat_schedule = {
    "full-report-task-crontab": {
        "task": "full_report",
        "schedule": crontab(
            hour=report_hours, minute=report_minutes, day_of_week="0-6"
        ),
    },
}
app.autodiscover_tasks()
