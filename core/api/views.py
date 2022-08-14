from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from core.api.serializers import *

### Category ###

#Create API
class CategortyAddAPi(CreateAPIView):
        serializer_class = CategorySerializers

#LIST API
class CategoryListApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def post(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = CategorySerializers(queryset, many=True)
        return Response(serializer.data)

#Edit API
class CategoryUpdateApi(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

#Delete Api
class CategoryDeleteApi(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers



# Product
class ProductListApi(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

# Client
class ClientListApi(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializers

# Provider
class ProviderListApi(ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializers

# Lot
class LotListApi(ListAPIView):
    queryset = Lot.objects.all()
    serializer_class = LotSerializers

# Stock
class StockListApi(ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializers

# User
class UserListApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
