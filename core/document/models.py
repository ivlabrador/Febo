from django.db import models
from django.forms import model_to_dict
import datetime as dt
from core.user.models import User
from config.validators import validate_file_extension

"""
DocCategory: Categorias de la documentacion
"""
class DocCategory(models.Model):
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

"""
DocStorage: Repositorio de documentacion empresarial
"""
class Document(models.Model):
    # Visual Attrs
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    category = models.ForeignKey(DocCategory, on_delete=models.CASCADE, verbose_name='Categoría')
    entity = models.CharField(max_length=150, verbose_name='Entidad', blank=True)
    started_at = models.DateField(verbose_name='Fecha', null=True, blank=True)
    expiration = models.DateField(verbose_name='Vencimiento', null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    file = models.FileField(upload_to='documentos/%Y/%m/%d', null=False, verbose_name='Archivo', validators=[validate_file_extension])
    # DataBase - Attrs
    is_active = models.BooleanField(default=True, verbose_name='¿Activo?')
    charger = models.ForeignKey(User, editable=True, on_delete=models.CASCADE, verbose_name='Cargado por ', null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Inserido en el sistema')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    def __str__(self):
        return f'{self.name} ({self.category})'

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        return item

    def is_active(self):
        today = dt.datetime.today().strftime('%Y-%m-%d')
        expiration = self.expiration
        if today == expiration:
            self.is_active = False
        else:
            self.is_active = True


    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-id']
