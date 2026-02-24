import json
import csv
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaccion
from .forms import TransaccionForm
from .services import calcular_resumen_financiero, get_gastos_por_categoria
from .reports import generar_pdf_finanzas

@login_required(login_url='login')
def dashboard(request):
    mes_seleccionado = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    try:
        anio, mes = map(int, mes_seleccionado.split('-'))
    except (ValueError, AttributeError):
        fecha_actual = timezone.now()
        anio, mes = fecha_actual.year, fecha_actual.month
        mes_seleccionado = f"{anio}-{mes:02d}"

    # Filtramos todo por request.user
    resumen = calcular_resumen_financiero(anio, mes, request.user)
    transacciones = Transaccion.objects.filter(user=request.user, fecha__year=anio, fecha__month=mes).order_by('-fecha')

    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.user = request.user # <--- Seguridad: Asignamos el dueño
            transaccion.save()
            messages.success(request, '¡Transacción guardada correctamente!')
            return redirect(f'/?mes={mes_seleccionado}')
    else:
        form = TransaccionForm(user=request.user)

    gastos_data = transacciones.filter(categoria__tipo='G').values('categoria__nombre').annotate(total=Sum('monto'))

    context = {
        'resumen': resumen,
        'transacciones': transacciones[:10],
        'form': form,
        'mes_actual': mes_seleccionado,
        'nombres_categorias': json.dumps([item['categoria__nombre'] for item in gastos_data]),
        'totales_categorias': json.dumps([float(item['total'] or 0) for item in gastos_data]),
        'gastos_por_categoria': get_gastos_por_categoria(request.user) # Asegúrate de que este servicio filtre por user
    }
    return render(request, 'finanzas/dashboard.html', context)

# ... (exportar_csv y descargar_reporte_pdf deben usar .filter(user=request.user))

