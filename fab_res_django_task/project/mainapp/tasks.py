from datetime import datetime
import json
import requests

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from pydantic import BaseModel

from .models import Message, Client, Mailing



class Task(BaseModel):
    client_id: int
    mailing_id: int
    phone_number: int
    message: str
    stop_time: datetime


class Msg(BaseModel):
    id: int
    phone: int
    text: str


def get_task_mailing(mailing, now=None):
    """
    Генерирует список задач на основе объекта рассылки и текущего времени.

    Args:
        mailing: Объект рассылки (Mailing).
        now: Текущее время (по умолчанию текущее серверное время).

    Returns:
        Генератор объектов Task.
    """
    if now is None:
        now = timezone.now()

    filter = mailing.client_filter
    clients = Client.objects.all()
    filter_key = "operator_code"
    if filter_key in filter:
        clients = clients.filter(operator_code=filter[filter_key])
    filter_key = "tag"
    if filter_key in filter:
        clients = clients.filter(operator_code=filter[filter_key])
    for client in clients:
        if (
                timezone.localtime(mailing.launch_date_time, client.time_zone)
                < timezone.localtime(now, client.time_zone)
                < timezone.localtime(mailing.end_date_time, client.time_zone)
        ):
            yield Task(
                client_id=client.id,
                mailing_id=mailing.id,
                phone_number=client.phone_number,
                message=mailing.text,
                stop_time=mailing.end_date_time
            )


def get_tasks_mailings():
    """
    Генерирует список задач для всех рассылок.

    Returns:
        Генератор объектов Task.
    """
    now = timezone.now()
    for mailing in Mailing.objects.all():
        yield from get_task_mailing(mailing, now)


@shared_task()
def client_notification(task_data):
    """
    Отправляет сообщение для клиента и обновляет статус сообщения.

    Args:
        task_data: Данные задачи в формате JSON.

    Raises:
        requests.Timeout: Если запрос превысил время ожидания.
    """
    task = Task.parse_obj(json.loads(task_data))
    message = Message(client_id=Client(task.client_id), mailing_id=Mailing(task.mailing_id))
    message.save()
    msg = Msg(id=message.id, phone=task.phone_number, text=task.message)
    try:
        response = requests.post(
            f"https://probe.fbrq.cloud/v1/send/{msg.id}",
            headers={"Authorization": f"Bearer {settings.JWT}"},
            json=msg.dict(),
            timeout=3,
        )
        response_text = response.text
        print(f"Response Text: {response_text}")
        message.status = response.status_code
    except requests.Timeout:
        message.status = 504  # Gateway Timeout
    message.save(update_fields=["status"])


def add_tasks(tasks):
    """
    Добавляет задачи в очередь для выполнения.

    Args:
        tasks: Список задач.

    """
    for task in tasks:
        client_notification.apply_async(args=[task.json()], expires=task.stop_time)


@shared_task()
def active_mailings_check():
    """
    Задачи, выполняемые по расписанию для поиска клиентов и текущего времени.
    """
    add_tasks(get_tasks_mailings())


def process_active_mailing(mailing_id):
    """
    Обрабатывает активную рассылку.

    Args:
        mailing_id: Идентификатор рассылки.

    """
    add_tasks(get_task_mailing(Mailing.objects.get(id=mailing_id)))
