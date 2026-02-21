from django.shortcuts import render
from .services import calcular_resumen_financiero
from .models import Transaccion

def dashboard(request):
    resumen = calcular_resumen_financiero()
    transacciones = Transaccion.objects.all()[:10] # Las últimas 10
    
    context = {
        'resumen': resumen,
        'transacciones': transacciones
    }
    return render(request, 'finanzas/dashboard.html', context)

