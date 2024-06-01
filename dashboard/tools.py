import os
import datetime

from dotenv import load_dotenv
from asgiref.sync import sync_to_async

from .tasks import send_bot_report


load_dotenv()

report_time = os.getenv('REPORT_TIME')


@sync_to_async
def get_report_time():
    return report_time


@sync_to_async
def activate_report_timer():
    now = datetime.datetime.now()
    now_time = now.time()
    report_at = datetime.datetime.strptime(report_time, "%H:%M").time()
    if report_at >= now_time:
        hours, minutes = report_time.split(':')
        report_hours = int(hours)
        report_minutes = int(minutes)
        report_in_seconds = report_hours * 3600 + report_minutes * 60
        now_hours = now.hour
        now_minutes = now.minute
        now_in_seconds = now_hours * 3600 + now_minutes * 60
        seconds_left = report_in_seconds - now_in_seconds
        send_bot_report.apply_async(countdown=seconds_left)
