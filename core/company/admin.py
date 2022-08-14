from django.contrib import admin
from .models import Company
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'fiscal_number']
    list_display = ['name', 'fiscal_number', 'email', 'address']


admin.site.register(Company, CompanyAdmin)