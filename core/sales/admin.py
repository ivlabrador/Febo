"""
from django.contrib import admin
from .models import Sale
# Register your models here.
class SaleAdmin(admin.ModelAdmin):
    search_fields = ['client', 'created_at']
    list_display = ['company', 'client', 'total', 'created_at']


admin.site.register(Sale,SaleAdmin)
"""