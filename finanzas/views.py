import json
import csv
from datetime import datetime
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from .models import Transaccion
from .forms import TransaccionForm
from .services import calcular_resumen_financiero
from .reports import generar_pdf_finanzas

def dashboard(request):
    # Obtener mes/año del filtro o usar el actual
    mes_seleccionado = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    
    try:
        anio, mes = map(int, mes_seleccionado.split('-'))
    except (ValueError, AttributeError):
        # Fallback al mes actual si hay error en el formato
        fecha_actual = timezone.now()
        anio, mes = fecha_actual.year, fecha_actual.month
        mes_seleccionado = f"{anio}-{mes:02d}"

    # Lógica de cálculo y transacciones filtradas
    resumen = calcular_resumen_financiero(anio, mes)
    transacciones = Transaccion.objects.filter(fecha__year=anio, fecha__month=mes).order_by('-fecha')

    # Manejo del formulario
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/?mes={mes_seleccionado}')
    else:
        form = TransaccionForm()

    # Datos para la gráfica
    gastos_data = Transaccion.objects.filter(fecha__year=anio, fecha__month=mes) \
        .values('categoria__nombre') \
        .annotate(total=Sum('monto'))

    nombres_categorias = [item['categoria__nombre'] for item in gastos_data]
    totales_categorias = [float(item['total'] or 0) for item in gastos_data]

    context = {
        'resumen': resumen,
        'transacciones': transacciones[:10], # Limitamos para el dashboard
        'form': form,
        'mes_actual': mes_seleccionado,
        'nombres_categorias': json.dumps(nombres_categorias),
        'totales_categorias': json.dumps(totales_categorias),
    }

    return render(request, 'finanzas/dashboard.html', context)

# ... [exportar_csv y descargar_reporte_pdf siguen igual]


def exportar_csv(request):
    """Genera un archivo CSV con todas las transacciones."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transacciones.csv"'

    writer = csv.writer(response)
    writer.writerow(['Descripcion', 'Monto', 'Fecha', 'Categoria'])

    # Obtenemos los datos
    transacciones = Transaccion.objects.all().values_list(
        'descripcion', 'monto', 'fecha', 'categoria__nombre'
    )

    for transaccion in transacciones:
        writer.writerow(transaccion)

    return response

def descargar_reporte_pdf(request):
    # 1. Obtenemos el mes del filtro o el actual
    mes_seleccionado = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    anio, mes = map(int, mes_seleccionado.split('-'))

    # 2. Obtenemos los datos necesarios
    context = {
        'resumen': calcular_resumen_financiero(anio, mes),
        'transacciones': Transaccion.objects.filter(fecha__year=anio, fecha__month=mes).order_by('-fecha'),
        'mes': mes_seleccionado
    }

    # 3. Llamamos a la función que genera el PDF
    return generar_pdf_finanzas(context)

