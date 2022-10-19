from django.urls import path

from core.user.views import *

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('add-user/', CreateUser.as_view(), name='add-user'),
    path('list-user/', ListUser.as_view(), name='list-user'),
    path('update-user/<int:pk>', UpdateUser.as_view(), name='update-user'),
    path('delete-user/<int:pk>', DeleteUser.as_view(), name='delete-user'),
    path('change-password/', UserChangePassword.as_view(), name='user-change-password'),
    path('edit-profile/', UpdateUserProfile.as_view(), name='update-user-profile'),
    path('choose/profile/<int:pk>/', SelectGroup.as_view(), name='select-group'),
]