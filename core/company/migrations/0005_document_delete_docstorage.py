# Generated by Django 4.0.6 on 2022-12-12 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0004_doccategory_docstorage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('entity', models.CharField(blank=True, max_length=150, verbose_name='Entidad')),
                ('started_at', models.DateField(blank=True, null=True, verbose_name='Fecha')),
                ('expiration', models.DateField(blank=True, null=True, verbose_name='Vencimiento')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
                ('payment_slip', models.FileField(blank=True, null=True, upload_to='document/%Y/%m/%d', verbose_name='Archivo')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizado')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.doccategory', verbose_name='Categoría')),
                ('charger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cargado por ')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
                'ordering': ['-id'],
            },
        ),
        migrations.DeleteModel(
            name='DocStorage',
        ),
    ]