from django.urls import path
from .views import create_client, update_client, delete_client

urlpatterns = [
    path('create/', create_client),
    path('update/', update_client),
    path('delete/', delete_client)
]

