from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from .serializers import ClientSerializer, MailingSerializer, MessageSerializer, MailingGeneralStatisticSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Mailing, Message
from rest_framework import generics


class ClientCreate(generics.CreateAPIView):
    serializer_class = ClientSerializer


class ClientUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["put", "delete", "patch"]


class MailingCreate(generics.CreateAPIView):
    serializer_class = MailingSerializer


class MailingGeneralStatisticsView(generics.ListAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingGeneralStatisticSerializer


class MailingUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    http_method_names = ["put", "delete", "patch"]


class MailingDetailedStatisticsView(generics.GenericAPIView):
    def get(self, request, pk):
        """Получение детальной статистики"""
        mailing_id = get_object_or_404(Mailing, id=pk)
        messages = Message.objects.filters(mailing_id=mailing_id)
        serialized_messages = MessageSerializer(messages, many=True).data
        return Response(serialized_messages, status.HTTP_200_OK)
