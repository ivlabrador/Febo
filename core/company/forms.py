from django import forms
from django.forms import ModelForm
from .models import Company
from bootstrap_datepicker_plus.widgets import DatePickerInput


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'f_name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre de fantasía'}),
            'fiscal_number': forms.TextInput(attrs={'placeholder': 'Ingrese un numero de CUIT'}),
            'activity': forms.TextInput(attrs={'placeholder': 'Ingrese la actividad principal'}),
            'started_at': DatePickerInput(format='%d-%m-%Y', attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'id': 'started_at',
                'type': 'date'
            }),
            'address': forms.TextInput(attrs={'placeholder': 'Calle - Bloque - Piso - Departamento - Numero '}),

            'phone_number': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'website': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'JPG - PNG'}),
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


