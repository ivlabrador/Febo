
from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.company.models import Company
from core.client.models import Client
from core.product.models import Product



class Sale(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_sale = models.DateField(auto_now=False, null=True, verbose_name='Fecha de venta')
    sale_num = models.CharField(max_length=10, null=False, verbose_name='Numero de factura')
    sale_type = models.CharField(choices=settings.SALE_TYPE, verbose_name='Tipo', null=True, max_length=1, default='A')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    created_at = models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    def __str__(self):
        txt = f"""
        Factura N°{self.sale_num} - tipo: {self.sale_type}
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
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['client'] = self.client.toJSON()
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['saleproduct'] = [i.toJSON() for i in self.saleproduct_set.all()]
        return item


    def delete(self, using=None, keep_parents=False):
        for detail in self.saleproduct_set.filter(product__is_inventoried=True):
            detail.product.stock += detail.cant
            detail.product.save()
        super(Sale, self).delete()

    def calculate_invoice(self):
        subtotal = self.saleproduct_set.all().aggregate(result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']



class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default=None, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=0)
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
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['id']
