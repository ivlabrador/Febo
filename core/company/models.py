from django.db import models
from config import settings
from django.forms import model_to_dict

class Company(models.Model):
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    f_name = models.CharField(max_length=150, verbose_name='Nombre de fantasía')
    fiscal_number = models.CharField(max_length=11, verbose_name='CUIT')
    activity = models.CharField(max_length=150, verbose_name='Activdad')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    phone_number = models.CharField(max_length=10, verbose_name='Teléfono')
    email = models.EmailField(max_length=50, verbose_name='Correo electrónico')
    website = models.CharField(max_length=150, verbose_name='Website')
    image = models.ImageField(upload_to='company/%d/%m/%Y', null=True, blank=True, verbose_name='Imagen')
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
