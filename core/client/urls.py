from django.urls import path

from .views import AddClient, ListClient, DeleteClient, UpdateClient

urlpatterns = [
    path('add-client/', AddClient.as_view(), name='add-client'),
    path('list-client/', ListClient.as_view(), name='list-client'),
    path('update-client/<int:pk>', UpdateClient.as_view(), name='update-client'),
    path('delete-client/<int:pk>', DeleteClient.as_view(), name='delete-client'),
]