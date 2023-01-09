from django.db import models
from config import settings
from django.forms import model_to_dict

"""
La clase COMPANY contiene toda la información que respecta a la empresa.
La misma información que AFIP. 
Version 1.0 FEBO contendrá solo una empresa por servidor.
El modelo esta sujeto a condiciones empresariales ARGENTINAS.
"""
class Company(models.Model):
    # Datos primarios - Identificaciones
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    f_name = models.CharField(max_length=150, verbose_name='Nombre de fantasía')
    fiscal_number = models.CharField(max_length=11, verbose_name='CUIT')
    activity = models.CharField(max_length=150, verbose_name='Actividad')
    iva_condition = models.CharField(choices=settings.IVA_CONDITION, verbose_name='Condición frente a IVA', null=False, blank=True, max_length=30)
    iibb = models.CharField(choices=settings.IIBB, verbose_name='Ingresos Brutos', null=False, blank=True,  max_length=30)
    started_at = models.DateField(verbose_name='Inicio de actividades', null=True, blank=True)
    # Datos secundarios - Localidad
    address = models.CharField(max_length=150, null=False, blank=True, verbose_name='Dirección')
    city = models.CharField(max_length=50, null=False, blank=True, verbose_name='Ciudad')
    state = models.CharField(max_length=50, null=False, blank=True, verbose_name='Provincia')
    postal = models.CharField(max_length=10, null=False, blank=True, verbose_name='Código postal')
    # Datos terciarios - Contacto
    phone_number = models.CharField(max_length=12, verbose_name='Teléfono')
    email = models.EmailField(max_length=50, verbose_name='Correo electrónico')
    website = models.CharField(max_length=150, verbose_name='Website')
    image = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Logo')
    created_at = models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/febo.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Compañía'
        verbose_name_plural = 'Compañías'
        default_permissions = ()
        permissions = (
            ('change_company', 'Can change Company'),
        )
        ordering = ['id']