from django.contrib import admin
from .models import Lot, Stock


class LotAdmin(admin.ModelAdmin):
    search_fields = ['product', 'charger']
    list_display = ['product', 'quantity', 'price', 'charger']
    list_filter = ['charger', ]

class StockAdmin(admin.ModelAdmin):
    search_fields = ['product', ]
    list_display = ['product', 'stock', 'is_active']

#Register
admin.site.register(Lot, LotAdmin)
admin.site.register(Stock, StockAdmin)