from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import get_object_or_404
from rest_framework import generics

from .models import Client, Mailing, Message
from .serializers import (
    ClientSerializer,
    MailingSerializer,
    MessageSerializer,
    MailingGeneralStatisticSerializer
)


class ClientCreate(generics.CreateAPIView):
    """
    Создание нового клиента.

    Serializer Class:
        ClientSerializer

    HTTP метод:
        POST
    """
    serializer_class = ClientSerializer


class ClientUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
     Получение, обновление и удаление информации о клиенте по его идентификатору.

     Serializer Class:
         ClientSerializer

     HTTP методы:
         GET, PUT, PATCH, DELETE
     """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["put", "delete", "patch"]


class MailingCreate(generics.CreateAPIView):
    """
    Создание новой рассылки.

    Serializer Class:
        MailingSerializer

    HTTP метод:
        POST
    """
    serializer_class = MailingSerializer


class MailingGeneralStatisticsView(generics.ListAPIView):
    """
    Получение общей статистики по рассылкам.

    Serializer Class:
        MailingGeneralStatisticSerializer

    HTTP метод:
        GET
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingGeneralStatisticSerializer


class MailingUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление информации о рассылке по ее идентификатору.

    Serializer Class:
        MailingSerializer

    HTTP методы:
        GET, PUT, PATCH, DELETE
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    http_method_names = ["put", "delete", "patch"]


class MailingDetailedStatisticsView(generics.GenericAPIView):
    """
    Получение детальной статистики по рассылке по ее идентификатору.

    Serializer Class:
        MessageSerializer (Пожалуйста, уточните подходящий сериализатор)

    HTTP метод:
        GET
    """
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get(self, request, pk):
        """
        Получение детальной статистики по рассылке.

        Args:
            request: Запрос HTTP.
            pk: Идентификатор рассылки.

        Returns:
            Response: JSON-ответ с детальной статистикой сообщений.
        """
        mailing_id = get_object_or_404(Mailing, id=pk)
        messages = Message.objects.filter(mailing_id=mailing_id)
        serialized_messages = MessageSerializer(messages, many=True).data
        return Response(serialized_messages, status.HTTP_200_OK)
