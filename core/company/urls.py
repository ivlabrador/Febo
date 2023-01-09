from django.urls import path

from .views import CreateCompany, UpdateCompany
urlpatterns = [
    # Company
    path('add-company/', CreateCompany.as_view(), name='add-company'),
    path('update-company/<int:pk>', UpdateCompany.as_view(), name='update-company')
]