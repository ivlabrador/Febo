from django import forms
from django.forms import ModelForm

# Date Range
class ReportPurchaseForm(forms.Form):
    date_ranger = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))