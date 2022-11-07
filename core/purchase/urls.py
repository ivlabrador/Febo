from django.urls import path
from .views import ListPurchase, ReportPurchase, AddPurchase

urlpatterns = [
    # Sales
    path('add-purchase/', AddPurchase.as_view(), name='add-purchase'),
    path('list-purchase/', ListPurchase.as_view(), name='list-purchase'),
    #path('update-sale/<int:pk>', UpdateSale.as_view(), name='update-sale'),
    #path('delete-sale/<int:pk>', DeleteSale.as_view(), name='delete-sale'),
    path('report-purchase/', ReportPurchase.as_view(), name='report-purchase'),
]