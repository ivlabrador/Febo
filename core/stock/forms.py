from django.forms import ModelForm
from .models import Lot
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from config import settings

class LotForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Lot
        fields = 'product', 'lot_date', 'provider', 'pay_condition', 'price', 'quantity', 'is_pay', 'payment_slip'
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select-sm'}),
            'lot_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'provider': forms.Select(attrs={'class': 'form-select-sm'}),
            'pay_condition': forms.Select(attrs={'class': 'form-select-sm'}),
            #'price': forms.NumberInput(),
            #'quantity': forms.NumberInput(),
            'is_pay': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'payment_slip': forms.FileInput(attrs={'class': 'form-control'}),
        }