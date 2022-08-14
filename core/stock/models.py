from django.db import models
from core.sql_django.models import ListField
from core.product.models import Product
from core.user.models import User
from django.forms import model_to_dict
from core.provider.models import Provider
from config import settings

# Lot model

class Lot(models.Model):
    product = models.ForeignKey(Product, editable=True, on_delete=models.CASCADE, verbose_name='Producto')
    lot_date = models.DateField(auto_now=False, null=True, verbose_name='Fecha de compra')
    provider = models.ForeignKey(Provider, default=None, verbose_name='Proveedor', blank=True, on_delete=models.CASCADE)
    pay_condition = models.CharField(choices=settings.PAY_CONDITION, verbose_name='Condición de pago', null=True, max_length=10, default='30')
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo neto U.')
    quantity = models.IntegerField(default=0, null=False, verbose_name='Cantidad')
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Total', null=True) #Al momneto null=True  por prueba igual en charger
    payment_slip = models.FileField(upload_to='pdf', null=True, blank=True, verbose_name='Factura de compra')
    is_pay = models.BooleanField(default=False, verbose_name='¿Pagado?')
    charger = models.ForeignKey(User, editable=True, on_delete=models.CASCADE, verbose_name='Cargado por', null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        default_permissions = ()
        permissions = (
            ('change_lot', 'Can change Lot'),
        )
        ordering = ['id']


# Stock Model

class Stock(models.Model):
    product = models.ForeignKey(Product, editable=True, on_delete=models.CASCADE, verbose_name='Producto')
    lots = ListField(default=[], editable=True, verbose_name='Lotes cargados')
    stock = models.IntegerField(default=0, null=False, verbose_name='Cantidad en stock')
    is_active = models.BooleanField(default=False)
    quantity_sold = models.IntegerField(default=0, null=False, verbose_name='Vendidos') # Aca deberia poner las ventas
    created_at = models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ultimo movimiento')

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self)
        return item


    def save(self, *args, **kwargs):
        stock = int(self.stock)
        if stock > 0:
            self.is_active = True
            return super(Stock, self).save(*args, **kwargs)
        elif stock == 0:
            self.is_active = False
            return super(Stock, self).save(*args, **kwargs)
        else:
            pass

    class Meta:
        default_permissions = ()
        permissions = (
            ('change_stock', 'Can change Stock'),
        )
        ordering = ['id']