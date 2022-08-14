from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ['name', 'description', 'created_at']

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'model']
    list_display = ['name', 'brand', 'model', 'is_active']
    list_filter = ['category', ]

#Register
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)