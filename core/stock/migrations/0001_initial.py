# Generated by Django 4.0.6 on 2022-08-12 09:33

import core.sql_django.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '__first__'),
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lots', core.sql_django.models.ListField(default=[], token=',', verbose_name='Lotes cargados')),
                ('stock', models.IntegerField(default=0, verbose_name='Cantidad en stock')),
                ('is_active', models.BooleanField(default=False)),
                ('quantity_sold', models.IntegerField(default=0, verbose_name='Vendidos')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ultimo movimiento')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Producto')),
            ],
            options={
                'ordering': ['id'],
                'permissions': (('change_stock', 'Can change Stock'),),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot_date', models.DateField(null=True, verbose_name='Fecha de compra')),
                ('pay_condition', models.CharField(choices=[(30, '30'), (60, '60'), (90, '90')], max_length=10, verbose_name='Condición de pago')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de compra')),
                ('quantity', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Total')),
                ('payment_slip', models.FileField(null=True, upload_to='', verbose_name='Factura de compra')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizado')),
                ('charger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cargado por')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Producto')),
                ('provider', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='provider.provider', verbose_name='Proveedor')),
            ],
            options={
                'verbose_name': 'Lote',
                'verbose_name_plural': 'Lotes',
                'ordering': ['id'],
                'permissions': (('change_lot', 'Can change Lot'),),
                'default_permissions': (),
            },
        ),
    ]