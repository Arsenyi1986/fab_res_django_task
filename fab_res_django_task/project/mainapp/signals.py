from datetime import datetime
from .tasks import process_active_mailing
from pytz import utc


def mailing_create_signal(sender, instance, created, **kwargs):
    """Сигнал о создании рассылки"""
    if created and instance.launch_datetime < datetime.now(utc):
        process_active_mailing.apply_async(args=[instance.unique_id])

