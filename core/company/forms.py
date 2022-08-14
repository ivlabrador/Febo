from django import forms
from django.forms import ModelForm
from .models import Company


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
            'fiscal_number': forms.TextInput(attrs={'placeholder': 'Ingrese un numero de CUIT'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'activity': forms.TextInput(attrs={'placeholder': 'Ingrese la actividad principal'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'website': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
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