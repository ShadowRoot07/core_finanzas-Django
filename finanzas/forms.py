from django import forms
from .models import Transaccion, Categoria, Cuenta

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

    def __init__(self, *args, **kwargs):
        # Capturamos el usuario desde los kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filtramos los select para que el usuario solo elija lo suyo
            self.fields['cuenta'].queryset = Cuenta.objects.filter(user=user)
            self.fields['categoria'].queryset = Categoria.objects.filter(user=user)

