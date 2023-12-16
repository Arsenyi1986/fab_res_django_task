import json
import requests
from .models import Message, Client, Mailing
from pydantic import BaseModel
from celery import shared_task
from datetime import datetime


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
    filter = mailing.client_filter
    clients = Client.objects.all()
    filter_key = "operator_code"
    if filter_key in filter:
        clients = clients.filter(operator_code=filter[filter_key])
    filter_key = "tag"
    if filter_key in filter:
        clients = clients.filter(operator_code=filter[filter_key])
    for client in clients:
        if



def get_tasks_mailings():
    now = datetime.now()
    for mailing in Mailing.objects.all():



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


def active_mailings_check():
    add_tasks()
