# Generated by Django 4.0.6 on 2022-08-12 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Razón Social')),
                ('f_name', models.CharField(max_length=150, verbose_name='Nombre de fantasía')),
                ('fiscal_number', models.CharField(max_length=11, verbose_name='CUIT')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Dirección')),
                ('phone_number', models.CharField(max_length=10, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=50, verbose_name='Correo electrónico')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizado')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['id'],
                'permissions': (('change_client', 'Can change Client'),),
                'default_permissions': (),
            },
        ),
    ]
