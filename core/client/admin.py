from django.contrib import admin
from .models import Client
# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['name', 'fiscal_number']
    list_display = ['name', 'fiscal_number', 'email', 'address']


admin.site.register(Client, ClientAdmin)
