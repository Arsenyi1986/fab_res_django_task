import json
import requests
from .models import Message, Client, Mailing
from pydantic import BaseModel
from celery import shared_task
from datetime import datetime
from django.utils import timezone


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


def get_task_mailing(mailing, now_time=datetime.now()):
    """Генерация списка задач по переданному объекту рассылки на основе заданных рассылок и текущего времени"""
    filter = mailing.client_filter
    clients = Client.objects.all()
    filter_key = "operator_code"
    if filter_key in filter:
        clients = clients.filter(operator_code=filter[filter_key])
    filter_key = "tag"
    if filter_key in filter:
        clients = clients.filter(operator_code=filter[filter_key])
    for client in clients:
        if (timezone.localtime(mailing.launch_date_time, client.time_zone)
           < timezone.localtime(now_time, client.time_zone)
           < timezone.localtime(mailing.end_date_time, client.time_zone)):
            yield Task(
                client_id=client.unique_id,
                mailing_id=mailing.unique_id,
                phone_number=client.phone_number,
                message=mailing.text,
                stop_time=mailing.end_date_time
            )


def get_tasks_mailings():
    """Генерация списка задач для всех рассылок"""
    now = datetime.now()
    for mailing in Mailing.objects.all():
        yield from get_task_mailing(mailing, now)


@shared_task()
def client_notification(task_data):
    """Отправка сообщения для клиента"""
    task = Task.parse_obj(json.loads(task_data))
    message = Message(client_id=Client(task.client_id), mailing_id=Mailing(task.mailing_id))
    message.save()
    msg = Msg(id=message.unique_id, phone=task.phone_number, text=task.message)
    try:
        response = requests.post(
            f"https://probe.fbrq.cloud/v1/send/{msg.id}",
            headers={"Authorization": f"Bearer {settings.JWT}"},
            # json=
        )
        message.status = response.status_code
    except requests.Timeout:
        message.status = 504    # Gateway Timeout
    message.save(update_fields=["status"])


def add_tasks(tasks):
    for task in tasks:
        client_notification.apply_async(args=[task.json()])


@shared_task()
def active_mailings_check():
    """Задачи запускаемые по расписанию (ищет клиентов для отправки, а также текущее время)"""
    add_tasks(get_tasks_mailings())


def process_active_mailing(mailing_unique_id):
    add_tasks(get_task_mailing(Mailing.objects.get(unique_id=mailing_unique_id)))
