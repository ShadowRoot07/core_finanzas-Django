from django.shortcuts import render, redirect
from .services import calcular_resumen_financiero
from .models import Transaccion
from .forms import TransaccionForm
from .services import calcular_resumen_financiero, get_gastos_por_categoria
import json
from django.core.serializers.json import DjangoJSONEncoder

def dashboard(request):
    resumen = calcular_resumen_financiero()
    transacciones = Transaccion.objects.all()[:10]
    
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigimos para evitar que el formulario se envíe dos veces al refrescar
            return redirect('dashboard') 
    else:
        form = TransaccionForm() 
    
    gastos_data = get_gastos_por_categoria()

    nombres_categorias = [item['categoria__nombre'] for item in gastos_data]
    totales_categorias = [float(item['total']) for item in gastos_data]
   
    context = {
        'resumen': resumen,                   # Agregado
        'transacciones': transacciones,       # Agregado
        'gastos_por_categoria': gastos_data,  # Agregado
        'form': form,                         # Agregado
        'nombres_categorias': json.dumps(nombres_categorias),
        'totales_categorias': json.dumps(totales_categorias),
    }
    
    return render(request, 'finanzas/dashboard.html', context)
