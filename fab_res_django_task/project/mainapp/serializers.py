from rest_framework import serializers
from .models import Mailing, Client, Message


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MailingGeneralStatisticSerializer(MailingSerializer):
    sending_status = serializers.SerializerMethodField()

    def get_sending_status(self, mailing):
        statistics = {}
        messages = Message.objects.filter(mailing=mailing)
        for message in messages:
            if message.sending_status in statistics:
                statistics[message.sending_status]["sent messages count"] += 1
            else:
                statistics[message.sending_status] = dict(sent_messages_count=1)
        return statistics
    class Meta:
        model = Mailing
        fields = (
            *(field.name for field in model._meta.fields),
        )


class ClientPropertyFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "operator_code", "tag"
        extra_kwargs = {field: dict(required=False) for field in fields}
