from django.db import models
from django.forms import model_to_dict


# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    f_name = models.CharField(max_length=150, verbose_name='Nombre de fantasía')
    fiscal_number = models.CharField(max_length=11, verbose_name='CUIT')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    phone_number = models.CharField(max_length=10, verbose_name='Teléfono')
    email = models.EmailField(max_length=50, verbose_name='Correo electrónico')
    created_at = models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        default_permissions = ()
        permissions = (
            ('change_provider', 'Can change Provider'),
        )
        ordering = ['id']
