from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.forms import ModelForm

# Purchase Form
from core.purchase.models import Purchase


class PurchaseForm(ModelForm):

    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'company': forms.Select(attrs={
                'class': 'form-control',
            }),
            'provider': forms.Select(attrs={
                'class': 'form-control',
            }),
            'buy_num': forms.TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
            }),
            'buy_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date': DatePickerInput(format='%d-%m-%Y', attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'id': 'date_sale',
                'type': 'date'
            }),
            'pay_condition': forms.Select(attrs={
                'class': 'form-control',
            }),
            'pay_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'total_discount': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'total_iva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'is_pay': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'payment_slip': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }


# Date Range
class ReportPurchaseForm(forms.Form):
    date_ranger = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))