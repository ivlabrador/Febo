from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import DocCategory, Document
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from config import settings as s

class DocCategoryForm(ModelForm):
    class Meta:
        model = DocCategory
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class DocumentForm(ModelForm):

    max_size = s.FILE_UPLOAD_MAX_MEMORY_SIZE

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            if file.size > self.max_size:
                raise ValidationError("El tamaño del archivo supera los 5Mb")
            return file
        else:
            raise ValidationError('El archivo no se puede leer')

    class Meta:
        model = Document
        fields = ('name', 'category', 'entity', 'started_at', 'expiration', 'description', 'file')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
            'entity': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
            'started_at': DatePickerInput(format='%d-%m-%Y', attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'id': 'started_at',
                'type': 'date',
                'required': 'true'
            }),
            'expiration': DatePickerInput(format='%d-%m-%Y', attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'id': 'started_at',
                'type': 'date',
                'required': 'true'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
        }

    def save(self, user, commit=True):
        data = {}
        instance = super(DocumentForm, self).save(commit=False)
        try:
            if instance:
                instance.charger_id = user
                instance.save()
            else:
                data['error'] = instance.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class SendFileForm(ModelForm):
    class Meta:
        fields = ['email', 'description']