from django.urls import path

from .views import AddLot, ListLot, ListStock, UpdateLot, DeleteLote

urlpatterns = [
    # Lots
    path('add-lot/', AddLot.as_view(), name='add-lot'),
    path('list-lot/', ListLot.as_view(), name='list-lot'),
    path('update-lot/<int:pk>', UpdateLot.as_view(), name='update-lot'),
    path('delete-lot/<int:pk>', DeleteLote.as_view(), name='delete-lot'),
    # Stock
    path('list-stock/', ListStock.as_view(), name='list-stock'),
]