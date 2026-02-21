from django import forms
from .models import Transaccion

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['cuenta', 'categoria', 'monto', 'descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'monto': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'cuenta': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'categoria': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }

