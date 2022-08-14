from django.urls import path
# Views of categories
from .views import CreateCategory, ListCategory, UpdateCategory, DeleteCategory
# Vies of products
from .views import CreateProduct, ListProduct, UpdateProduct, DeleteProduct

urlpatterns = [
    # Category
    path('add-category/', CreateCategory.as_view(), name='add-category'),
    path('list-category/', ListCategory.as_view(), name='list-category'),
    path('update-category/<int:pk>/', UpdateCategory.as_view(), name='update-category'),
    path('delete-category/<int:pk>/', DeleteCategory.as_view(), name='delete-category'),
    # Product
    path('add-product/', CreateProduct.as_view(), name='add-product'),
    path('list-product/', ListProduct.as_view(), name='list-product'),
    path('update-product/<int:pk>/', UpdateProduct.as_view(), name='update-product'),
    path('delete-product/<int:pk>', DeleteProduct.as_view(), name='delete-product'),
]