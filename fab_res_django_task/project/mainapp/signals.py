from datetime import datetime
from .tasks import process_active_mailing
from pytz import utc


def mailing_create_signal(sender, instance, created, **kwargs):
    """
    Сигнал о создании рассылки.

    Args:
        sender: Отправитель сигнала (модель рассылки).
        instance: Экземпляр модели рассылки.
        created: Флаг, указывающий, был ли создан экземпляр (True/False).
        **kwargs: Дополнительные аргументы, переданные с сигналом.

    Description:
        Этот сигнал вызывается при создании экземпляра модели рассылки.
        Если рассылка создана и ее дата запуска меньше текущей даты и времени в часовом поясе UTC,
        то запускается асинхронная задача process_active_mailing для обработки активной рассылки.
    """
    if created and instance.launch_datetime < datetime.now(utc):
        process_active_mailing.apply_async(args=[instance.id])
