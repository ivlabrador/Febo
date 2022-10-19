from django.db import models
from django.forms import model_to_dict


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    f_name = models.CharField(max_length=150, verbose_name='Nombre de fantasía')
    fiscal_number = models.CharField(max_length=11, verbose_name='CUIT')
    iva_condition = models.CharField(max_length=150, verbose_name='Condición de Iva')
    phone_number = models.CharField(max_length=10, verbose_name='Teléfono')
    email = models.EmailField(max_length=50, verbose_name='Correo electrónico')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    city = models.CharField(max_length=150, null=True, blank=True, verbose_name='Ciudad')
    state = models.CharField(max_length=150, null=True, blank=True, verbose_name='Provincia')
    created_at = models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def get_full_address(self):
        address = f'{self.address}, {self.city}, {self.state}'
        return address

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        default_permissions = ()
        permissions = (
            ('change_client', 'Can change Client'),
        )
        ordering = ['-id']
