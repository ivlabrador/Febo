from django import forms
from django.forms import ModelForm
from .models import Sale, SalePoint
from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import datetime

from ..client.models import Client

class SalePointForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = SalePoint
        fields = '__all__'
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['client'].queryset = Client.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={
                'class': 'custom-select select2',
            }),
            'date_sale': DatePickerInput(format='%d-%m-%Y', attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'id': 'date_sale',
                'type': 'date'
            }
                                           ),
            'sale_point': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sale_point',
            }),
            'sale_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sale_type',
            }),
            'sale_num': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'sale_num',
            }),
            'pay_condition': forms.Select(attrs={
                'class': 'form-control',
                'id': 'pay_condition',
            }),
            'pay_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'pay_type',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total_discount': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total_iva': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }
