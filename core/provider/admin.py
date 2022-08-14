from django.contrib import admin
from .models import Provider
# Register your models here.
class ProviderAdmin(admin.ModelAdmin):
    search_fields = ['name', 'fiscal_number']
    list_display = ['name', 'fiscal_number', 'email', 'address']


admin.site.register(Provider,ProviderAdmin)