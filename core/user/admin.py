from django.contrib import admin
from core.user.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    search_fields = ("username", "first_name", "last_name", "email")

title = "Febo App"
subtitle = "Panel de Gestion"
admin.site.site_header =title
admin.site.site_title = title
admin.site.index_title = subtitle

admin.site.register(User, UserAdmin)