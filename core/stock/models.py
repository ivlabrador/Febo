from django.db import models

from core.purchase.models import Purchase
from core.sql_django.models import ListField
from core.product.models import Product
from core.user.models import User
from django.forms import model_to_dict
from core.provider.models import Provider
from config import settings
from core.company.models import Company
import datetime as dt
# Lot model

class Lot(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, default=None, verbose_name='Proveedor', blank=True, on_delete=models.CASCADE)
    lot_date = models.DateField(auto_now=False, null=True, verbose_name='Fecha de compra')
    buy_num = models.CharField(max_length=20, null=False, verbose_name='Numero de factura')
    buy_type = models.CharField(choices=settings.SALE_TYPE, verbose_name='Tipo', null=True, max_length=1, default='A')
    pay_condition = models.CharField(choices=settings.PAY_CONDITION, verbose_name='Condición de pago', null=True, max_length=10, default='30')
    pay_type = models.CharField(choices=settings.PAY_TYPE, verbose_name='Tipo de pago', null=False, max_length=20, default='Efectivo')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_discount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    payment_slip = models.FileField(upload_to='compras/%Y/%m/%d', null=True, blank=True, verbose_name='Factura de compra')
    make_invoice = models.BooleanField(default=True, verbose_name='¿Cargar en compras?')
    is_pay = models.BooleanField(default=True, verbose_name='¿Pagado?')
    charger = models.ForeignKey(User, editable=True, on_delete=models.CASCADE, verbose_name='Cargado por', null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    def __str__(self):
        return self.buy_num

    def toJSON(self):
        item = model_to_dict(self)
        item['company'] = self.company.toJSON()
        item['provider'] = self.provider.toJSON()
        item['number'] = self.buy_num
        item['buy_type'] = f'{self.buy_type:.2f}'
        item['pay_type'] = f'{self.pay_type:.2f}'
        item['lot_date'] = self.lot_date.strftime('%d-%m-%Y')
        item['expiration'] = self.get_expiration_date.strftime('%d-%m-%Y')
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total_discount'] = f'{self.total_discount:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['lotproduct'] = [i.toJSON() for i in self.lotproduct_set.all()]
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        company = Company.objects.first()
        self.company = company

        if self.make_invoice:
            purchase = Purchase(
                company=self.company,
                provider=self.provider,
                buy_num=self.buy_num,
                buy_type=self.buy_type,
                date=self.lot_date,
                pay_condition=self.pay_condition,
                pay_type=self.pay_type,
                subtotal=self.subtotal,
                total_discount=self.total_discount,
                total_iva=self.total_iva,
                total=self.total,
                is_pay=self.is_pay,
                payment_slip=self.payment_slip,
                charger=self.charger
            )
            purchase.save()
        else:
            pass
        super(Lot, self).save()

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        default_permissions = ()
        permissions = (
            ('change_lot', 'Can change Lot'),
        )
        ordering = ['id']

    def get_expiration_date(self):
        date_sale = self.lot_date
        days = int(self.pay_condition)
        expiration = date_sale + dt.timedelta(days)
        return expiration


class LotProduct(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, default=None, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=0)
    discount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['quantity'] = f'{self.quantity:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Lote'
        verbose_name_plural = 'Detalle de Lotes'
        default_permissions = ()
        ordering = ['-id']


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
        item['product'] = self.product.toJSON()
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