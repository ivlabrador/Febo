from django.urls import path

from core.user.views import DashboardView, CreateUser, ListUser, UpdateUser, DeleteUser

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('add-user/', CreateUser.as_view(), name='add-user'),
    path('list-user/', ListUser.as_view(), name='list-user'),
    path('update-user/<int:pk>', UpdateUser.as_view(), name='update-user'),
    path('delete-user/<int:pk>', DeleteUser.as_view(), name='delete-user'),
]