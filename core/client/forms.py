from django import forms
from django.forms import ModelForm
from .models import Client

class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(),
            'fiscal_number': forms.TextInput(attrs={'type': 'number'}),
            'address': forms.TextInput(),
            'phone_number': forms.TextInput(attrs={'type': 'number'}),
            'email': forms.EmailInput()
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