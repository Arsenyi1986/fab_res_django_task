from rest_framework import serializers
from .models import Mailing, Client, Message
from .fields import ClientFilterSerializerField, TimeZoneSerializerField


class MailingSerializer(serializers.ModelSerializer):
    client_filter = ClientFilterSerializerField(default=dict)

    class Meta:
        model = Mailing
        fields = tuple(field.name for field in model._meta.fields)


class ClientSerializer(serializers.ModelSerializer):
    time_zone = TimeZoneSerializerField()

    class Meta:
        model = Client
        fields = tuple(field.name for field in model._meta.fields)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MailingGeneralStatisticSerializer(MailingSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, mailing):
        statistics = {}
        messages = Message.objects.filter(mailing=mailing)
        for message in messages:
            if message.sending_status in statistics:
                statistics[message.status]["sent messages count"] += 1
            else:
                statistics[message.status] = dict(sent_messages_count=1)
        return statistics

    class Meta:
        model = Mailing
        fields = (
            *(field.name for field in model._meta.fields),
            'status',  # Включите поле 'status' в список полей
        )


class ClientPropertyFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "operator_code", "tag"
        extra_kwargs = {field: dict(required=False) for field in fields}
