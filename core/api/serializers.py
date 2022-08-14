from rest_framework import serializers

from core.client.models import Client
from core.product.models import Category, Product


from core.provider.models import Provider
from core.stock.models import Lot, Stock
from core.user.models import User


# Category
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        return instance.toJSON()

#Products

class ProductSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


#Client
class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

#Provider
class ProviderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'



#Lot
class LotSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = '__all__'

#Stock
class StockSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

#User
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'