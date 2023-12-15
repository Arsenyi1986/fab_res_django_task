import uuid
from timezone_field import TimeZoneField
from django.db import models

# Create your models here.

MESSAGE_CHOICES = (
    ("Not sent", "Not sent"),
    ("In progress", "In progress"),
    ("Sent", "Sent")
)


class Mailing(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False, verbose_name='Уникальный id рассылки')
    launch_date_time = models.DateTimeField(verbose_name='дата и время запуска рассылки')
    text = models.TextField(verbose_name="текст сообщения для доставки клиенту")
    client_filter = models.JSONField(default=dict, blank=True, verbose_name="фильтр свойств клиентов")
    end_date_time = models.DateTimeField(verbose_name="дата и время окончания рассылки")

    def clean(self):
        super().clean()
        from .serializers import ClientPropertyFilterSerializer
        filter = self.client_filter
        assert filter.keys() <= set(ClientPropertyFilterSerializer.Meta.fields)
        ClientPropertyFilterSerializer(data=filter).is_valid(raise_exception=True)

    def __str__(self):
        return f"Рассылка {self.unique_id}"


class Client(models.Model):
    unique_id = models.AutoField(primary_key=True, verbose_name="уникальный id клиента")
    phone_number = models.CharField(max_length=11, verbose_name="номер телефона клиента")
    operator_code = models.CharField(max_length=10, verbose_name="код мобильного оператора")
    tag = models.CharField(max_length=255, verbose_name="тэг")
    time_zone = TimeZoneField(choices_display="WITH_GMT_OFFSET")

    def __str__(self):
        return f"Клиент {self.unique_id}"


class Message(models.Model):
    unique_id = models.AutoField(primary_key=True, verbose_name="уникальный id сообщения")
    create_date_time = models.DateTimeField(verbose_name='дата и время создания (отправки)')
    status = models.CharField(max_length=255, verbose_name="статус отправки",
                              choices=MESSAGE_CHOICES)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE,
                                   verbose_name="id рассылки, в рамках которой было отправлено сообщение")
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE,
                                  verbose_name="id клиента, которому отправили")

    def __str__(self):
        return f"Сообщение {self.unique_id}"
