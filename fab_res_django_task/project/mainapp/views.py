from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from .serializers import ClientSerializer, MailingSerializer, MessageSerializer, MailingGeneralStatisticSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Mailing, Message
from rest_framework import generics

# @api_view(["POST"])
# def create_client(request):
#     serializer = ClientSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientCreate(generics.CreateAPIView):
    serializer_class = ClientSerializer


class ClientUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["put", "delete", "patch"]


class MailingCreate(generics.CreateAPIView):
    serializer_class = MailingSerializer


class MailingUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    http_method_names = ["put", "delete", "patch"]


class MailingDetailedStatisticsView(generics.GenericAPIView):
    def get(self, request, pk):
        """Получение детальной статистики"""
        mailing = get_object_or_404(Mailing, id=pk)
        messages = Message.objects.filters(mailing=mailing)
        serialized_messages = MessageSerializer(messages, many=True).data
        return Response(serialized_messages, status.HTTP_200_OK)


class MailingGeneralStatisticsView(generics.ListAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingGeneralStatisticSerializer

# @api_view(["PUT"])
# def update_client(request, pk):
#     try:
#         client = Client.objects.get(pk=pk)
#     except Client.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     serializer = ClientSerializer(client, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["DELETE"])
# def delete_client(request, pk):
#     try:
#         client = Client.objects.get(pk=pk)
#     except Client.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     client.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["POST"])
# def create_mailing(request):
#     serializer = MailingSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["PUT"])
# def update_mailing(request, pk):
#     try:
#         mailing = Mailing.objects.get(pk=pk)
#     except Mailing.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     serializer = MailingSerializer(mailing, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["DELETE"])
# def delete_mailing(request, pk):
#     try:
#         mailing = Mailing.objects.get(pk=pk)
#     except Mailing.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     mailing.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)



# добавления новой рассылки со всеми её атрибутами +
#
# получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
#
# получения детальной статистики отправленных сообщений по конкретной рассылке
#
# обновления атрибутов рассылки +
#
# удаления рассылки +
#
# обработки активных рассылок и отправки сообщений клиентам