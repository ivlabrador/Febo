from django.urls import path
from .views import AddSale, ListSale, UpdateSale, DeleteSale, AddSalePoint, MakePDFInvoice, ReportSale

urlpatterns = [
    # Sales
    path('add-sale/', AddSale.as_view(), name='add-sale'),
    path('list-sale/', ListSale.as_view(), name='list-sale'),
    path('update-sale/<int:pk>', UpdateSale.as_view(), name='update-sale'),
    path('delete-sale/<int:pk>', DeleteSale.as_view(), name='delete-sale'),
    path('make-invoice/<int:pk>', MakePDFInvoice.as_view(), name='make-invoice'),
    # Sales - Point
    path('add-sale-point/', AddSalePoint.as_view(), name='add-sale-point'),
    # Sales - Report
    path('report-sale/', ReportSale.as_view(), name='report-sale'),

]

