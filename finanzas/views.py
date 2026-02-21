import json
import csv
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from .models import Transaccion
from .forms import TransaccionForm
from .services import calcular_resumen_financiero, get_gastos_por_categoria

def dashboard(request):
    # 1. Obtener mes/año del filtro o usar el actual
    mes_seleccionado = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    anio, mes = map(int, mes_seleccionado.split('-'))

    # 2. Lógica de cálculo y transacciones filtradas
    resumen = calcular_resumen_financiero(anio, mes)
    transacciones = Transaccion.objects.filter(fecha__year=anio, fecha__month=mes).order_by('-fecha')[:10]

    # 3. Manejo del formulario
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/?mes={mes_seleccionado}')
    else:
        form = TransaccionForm()

    # 4. Datos para la gráfica (filtrados)
    gastos_data = Transaccion.objects.filter(categoria__tipo='G', fecha__year=anio, fecha__month=mes) \
        .values('categoria__nombre') \
        .annotate(total=Sum('monto'))

    nombres_categorias = [item['categoria__nombre'] for item in gastos_data]
    totales_categorias = [float(item['total']) for item in gastos_data]

    # 5. Preparar contexto
    context = {
        'resumen': resumen,
        'transacciones': transacciones,
        'gastos_por_categoria': gastos_data,
        'form': form,
        'mes_actual': mes_seleccionado,
        'nombres_categorias': json.dumps(nombres_categorias),
        'totales_categorias': json.dumps(totales_categorias),
    }

    return render(request, 'finanzas/dashboard.html', context)

def exportar_csv(request):
    """
    Genera un archivo CSV con todas las transacciones.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transacciones.csv"'

    writer = csv.writer(response)
    writer.writerow(['Descripcion', 'Monto', 'Fecha', 'Categoria'])

    # Obtenemos los datos ordenados
    transacciones = Transaccion.objects.all().values_list(
        'descripcion', 'monto', 'fecha', 'categoria__nombre'
    )

    for transaccion in transacciones:
        writer.writerow(transaccion)

    return response

