from django.urls import path
from .views import AddDocument, AddDocCategory, ListDocument, UpdateDocument, DeleteDocument, DownloadFile, UpdateDocCategory, DeleteDocCategory, ListDocCategory, SendFile

urlpatterns = [
    # Doc - Category
    path('add-document-category/', AddDocCategory.as_view(), name='add-document-category'),
    path('list-document-category/', ListDocCategory.as_view(), name='list-document-category'),
    path('update-document-category/<int:pk>/', UpdateDocCategory.as_view(), name='update-document-category'),
    path('delete-document-category/<int:pk>', DeleteDocCategory.as_view(), name='delete-document-category'),
    # Document
    path('add-document/', AddDocument.as_view(), name='add-document'),
    path('list-document/', ListDocument.as_view(), name='list-document'),
    path('update-document/<int:pk>/', UpdateDocument.as_view(), name='update-document'),
    path('delete-document/<int:pk>', DeleteDocument.as_view(), name='delete-document'),
    path('send-document/<int:pk>', SendFile.as_view(), name='send-document'),
    # Otros
    path('download-document/<int:pk>/', DownloadFile.as_view(), name='download-file'),
]