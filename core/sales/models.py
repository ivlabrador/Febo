
from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict
import datetime as dt

from config import settings
from core.company.models import Company
from core.client.models import Client
from core.product.models import Product
from core.stock.models import Stock
from core.user.models import User

class SalePoint(models.Model):
    address = models.CharField(max_length=255, null=False, verbose_name='Domicilio de venta', unique=True)
    number = models.CharField(max_length=5, null=False, verbose_name='Número', unique=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.number

class Sale(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sale_point = models.ForeignKey(SalePoint, on_delete=models.CASCADE, verbose_name='Punto de venta')
    sale_num = models.CharField(max_length=20, null=False, verbose_name='Numero de factura')
    sale_type = models.CharField(choices=settings.SALE_TYPE, verbose_name='Tipo', null=True, max_length=1, default='A')
    date_sale = models.DateField(auto_now=False, null=True, verbose_name='Fecha de venta')
    pay_condition = models.CharField(choices=settings.PAY_CONDITION, verbose_name='Condición de pago', null=True, max_length=10, default='30')
    pay_type = models.CharField(choices=settings.PAY_TYPE, verbose_name='Tipo de pago', null=False, max_length=20, default='Efectivo')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_discount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    is_pay = models.BooleanField(default=False, verbose_name='¿Pagado?')
    charger = models.ForeignKey(User, editable=True, on_delete=models.CASCADE, verbose_name='Cargado por ', null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    def __str__(self):
        txt = f"""
        Factura N°{self.sale_point.number}-{self.sale_num} - tipo: {self.sale_type}
        Emisor: {self.company.name}
        Receptor: {self.client.name}
        """
        return txt

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Sale, self).save()

    def get_number(self):
        return f'{self.sale_point.number}-{self.sale_num}'

    def get_expiration_date(self):
        date_sale = self.date_sale
        days = int(self.pay_condition)
        expiration = date_sale + dt.timedelta(days)
        return expiration

    def toJSON(self):
        item = model_to_dict(self)
        item['company'] = self.company.toJSON()
        item['client'] = self.client.toJSON()
        item['number'] = self.get_number()
        item['sale_type'] = f'{self.sale_type:.2f}'
        item['date_sale'] = self.date_sale.strftime('%d-%m-%Y')
        item['expiration'] = self.get_expiration_date.strftime('%d-%m-%Y')
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total_discount'] = f'{self.total_discount:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['saleproduct'] = [i.toJSON() for i in self.saleproduct_set.all()]
        return item


    def delete(self, using=None, keep_parents=False):
        for detail in self.saleproduct_set.filter(product__is_active=True):
            stock = Stock.objects.get(product_id=detail.product.id)
            stock.stock += detail.quantity
            detail.product.save()
        super(Sale, self).delete()

    """
    No voy a usar esta funcion hasta que sea necesaria
    def calculate_invoice(self):
        subtotal = self.saleproduct_set.all().aggregate(result=Coalesce(Sum(F('price') * F('quantity')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        self.total_iva = (self.subtotal/100) * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()
    """
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']



class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default=None, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=0)
    discount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.name


    def save(self, *args, **kwargs):
        stock = Stock.objects.get(product_id=self.product.id)
        self.stock = stock
        return super(SaleProduct, self).save(args, **kwargs)



    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['stock'] = self.stock.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['quantity'] = f'{self.quantity:.2f}'
        item['discount'] = f'{self.subtotal:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['id']
