from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Identificar si es ingreso o gasto para facilitar reportes
    TIPO_CHOICES = [('I', 'Ingreso'), ('G', 'Gasto')]
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100) # Ejemplo: Banco Provincial, Efectivo
    saldo_inicial = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nombre} - {self.saldo_inicial}"


class Transaccion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']

