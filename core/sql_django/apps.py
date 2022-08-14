from django.apps import AppConfig


class SqlDjangoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.sql_django'
