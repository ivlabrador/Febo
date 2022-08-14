from django.urls import path
from .views import AddSale

urlpatterns = [
    # Provider
    path('add-sale/', AddSale.as_view(), name='add-sale'),
]

