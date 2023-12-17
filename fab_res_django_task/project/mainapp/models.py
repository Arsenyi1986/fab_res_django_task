from django.db import models
from timezone_field import TimeZoneField
from ujson import dumps
import itertools
from .utils import serialize_object


class BaseModel(models.Model):
    def __repr__(self):
        return dumps(
            self.to_dict(),
            indent=4,
            default=serialize_object,
            ensure_ascii=False,
            escape_forward_slashes=False,
        )

    def to_dict(self):
        data = {}
        options = self._meta
        for field in itertools.chain(options.concrete_fields, options.private_fields):
            data[field.name] = field.value_from_object(self)
        for field in options.many_to_many:
            data[field.name] = [i.id for i in field.value_from_object(self)]
        return data

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


MESSAGE_CHOICES = (
    ("Not sent", "Not sent"),
    ("In progress", "In progress"),
    ("Sent", "Sent")
)


class Mailing(BaseModel):
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
        return f"Рассылка {self.id}"


class Client(models.Model):
    phone_number = models.CharField(max_length=11, verbose_name="номер телефона клиента")
    operator_code = models.CharField(max_length=10, verbose_name="код мобильного оператора")
    tag = models.CharField(max_length=255, verbose_name="тэг")
    time_zone = TimeZoneField(choices_display="WITH_GMT_OFFSET")

    def __str__(self):
        return f"Клиент {self.id}"


class Message(models.Model):
    create_date_time = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                            verbose_name='дата и время создания (отправки)')
    status = models.CharField(max_length=255, verbose_name="статус отправки",
                              choices=MESSAGE_CHOICES)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE,
                                   verbose_name="id рассылки, в рамках которой было отправлено сообщение")
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE,
                                  verbose_name="id клиента, которому отправили")

    def __str__(self):
        return f"Сообщение {self.id}, Статус: {self.status}"
