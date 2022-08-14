# Generated by Django 4.0.6 on 2022-08-13 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0002_lot_is_pay_alter_lot_pay_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='charger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cargado por'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Costo neto U.'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, null=True, verbose_name='Total'),
        ),
    ]