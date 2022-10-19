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
        fields = '__all__'
        widgets = {
            'provider': forms.Select(attrs={
                'class': 'custom-select select2',
            }),
            'lot_date': forms.DateInput(format='%d-%m-%Y', attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'id': 'lot_date',
                'type': 'date'
            }
                                         ),
            'buy_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'buy_type',
            }),
            'pay_condition': forms.Select(attrs={
                'class': 'form-control',
                'id': 'pay_condition',
            }),
            'pay_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'pay_type',
            }),
            'buy_num': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'buy_num',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total_iva': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total_discount': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'payment_slip': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'make_invoice': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'is_pay': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


    # Save
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

