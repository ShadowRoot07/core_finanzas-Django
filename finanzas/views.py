from django.shortcuts import render, redirect
from django.db.models import Sum # Necesitas esto para el Sum en la vista
from .models import Transaccion
from .forms import TransaccionForm
from .services import calcular_resumen_financiero, get_gastos_por_categoria
import json
from django.utils import timezone

def dashboard(request):
    # 1. Obtener mes/año del GET o usar el actual
    mes_seleccionado = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    anio, mes = map(int, mes_seleccionado.split('-'))

    # 2. Llamar a las funciones pasando los parámetros necesarios
    resumen = calcular_resumen_financiero(anio, mes)
    transacciones = Transaccion.objects.filter(fecha__year=anio, fecha__month=mes).order_by('-fecha')[:10]

    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/?mes={mes_seleccionado}') # Mantenemos el filtro tras guardar
    else:
        form = TransaccionForm()

    # 3. Datos para la gráfica (filtrados)
    gastos_data = Transaccion.objects.filter(categoria__tipo='G', fecha__year=anio, fecha__month=mes) \
        .values('categoria__nombre') \
        .annotate(total=Sum('monto'))

    nombres_categorias = [item['categoria__nombre'] for item in gastos_data]
    totales_categorias = [float(item['total']) for item in gastos_data]

    context = {
        'resumen': resumen,
        'transacciones': transacciones,
        'gastos_por_categoria': gastos_data,
        'form': form,
        'nombres_categorias': json.dumps(nombres_categorias),
        'totales_categorias': json.dumps(totales_categorias),
        'mes_actual': mes_seleccionado, # Para que el input de fecha recuerde qué elegiste
    }

    return render(request, 'finanzas/dashboard.html', context)

