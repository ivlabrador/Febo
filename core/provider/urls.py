from django.urls import path
from .views import AddProvider, ListProvider, UpdateProvider, DeleteProvider

urlpatterns = [
    # Provider
    path('add-provider/', AddProvider.as_view(), name='add-provider'),
    path('list-provider/', ListProvider.as_view(), name='list-provider'),
    path('update-provider/<int:pk>', UpdateProvider.as_view(), name='update-provider'),
    path('delete-provider/<int:pk>', DeleteProvider.as_view(), name='delete-provider'),
]
