from django.urls import path
from core.api.views import *

urlpatterns = [
    # Category
    path('category/api-add', CategortyAddAPi.as_view(), name='api-category-add'),
    path('category/api-list', CategoryListApi.as_view(), name='api-category-list'),
    path('category/api-update/<int:pk>', CategoryUpdateApi.as_view(), name='api-category-update'),
    path('category/api-delete/<int:pk>', CategoryDeleteApi.as_view(), name='api-category-delete'),
    #Product
    path('product/api-list', ProductListApi.as_view(), name='api-product-list'),
    path('client/api-list', ClientListApi.as_view(), name='api-client-list'),
    path('provider/api-list', ProviderListApi.as_view(), name='api-provider-list'),
    path('lot/api-list', LotListApi.as_view(), name='api-lot-list'),
    path('stock/api-list', StockListApi.as_view(), name='api-stock-list'),
    path('user/api-list', UserListApi.as_view(), name='api-user-list'),
]