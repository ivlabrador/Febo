from django import forms
from django.forms import ModelForm
from .models import Sale, SaleProduct
from datetime import datetime

class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['client'].queryset = Client.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'client': forms.Select(),
            'date_sale': forms.DateInput(format='%d-%m-%Y', attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'id': 'date_joined',
                'type': 'date',
                'data-target': '#date_joined',
                'data-toggle': 'datetimepicker'
            }
                                           ),
            'sale_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'sale_num': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'iva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }
class ItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['client'].queryset = Client.objects.none()

    class Meta:
        model = SaleProduct
        fields = '__all__'
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }
