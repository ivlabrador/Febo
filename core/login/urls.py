from django.urls import path

from core.login.views import *

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('change-password-rst/<str:token>/', ChangePassword.as_view(), name='change-password')
]