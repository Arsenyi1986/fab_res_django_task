from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import ClientSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Client


@api_view(["POST"])
def create_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = ClientSerializer(client, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    client.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)