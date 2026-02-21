from django.shortcuts import render, redirect
from .services import calcular_resumen_financiero
from .models import Transaccion
from .forms import TransaccionForm
from .services import calcular_resumen_financiero, get_gastos_por_categoria
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from datetime import datetime

def dashboard(request):
    mes_seleccionado = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    anio, mes = map(int, mes_seleccionado.split('-'))
    resumen = calcular_resumen_financiero()
    transacciones = Transaccion.objects.filter(fecha__year=anio, fecha__month=mes).order_by('-fecha')

    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigimos para evitar que el formulario se envíe dos veces al refrescar
            return redirect('dashboard') 
    else:
        form = TransaccionForm() 
    
    gastos_data = Transaccion.objects.filter(categoria__tipo='G', fecha__year=anio, fecha__month=mes) \
        .values('categoria__nombre') \
        .annotate(total=Sum('monto'))

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
