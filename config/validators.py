import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Error en el formato del archivo, debe ser: "PDF, JPG o PNG"')


def validate_file_excel(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xls', '.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Error en el formato del archivo, debe ser: "XLS o XLSX"')