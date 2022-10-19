from django.db import models
from config import settings
from django.forms import model_to_dict


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    created_at = models.DateField(auto_now_add=True, null=False, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Actualizado")

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item


    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    brand = models.CharField(max_length=150, verbose_name='Marca', blank=True)
    model = models.CharField(max_length=50, verbose_name='Modelo', unique=True)
    iva = models.CharField(choices=settings.IVA_CONDITION, verbose_name='IVA', null=False, max_length=4)
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    category = models.ManyToManyField(Category, verbose_name='Categorías')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    is_active = models.BooleanField(default=True, verbose_name='¿Es activo?')
    created_at = models.DateField(auto_now_add=True, null=False, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Actualizado')

    def __str__(self):
        return f'{self.name} ({self.model})'

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = [i.toJSON() for i in self.category.all()]
        item['image'] = self.get_image()
        return item

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    def get_iva(self):
        if self.iva:
            iva = float(self.iva)
            return iva

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-id']
