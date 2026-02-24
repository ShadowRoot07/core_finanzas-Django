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
from .services import calcular_resumen_financiero, get_gastos_por_categoria, get_dashboard_data, crear_cuenta_para_usuario, crear_categoria_para_usuario
from .reports import generar_pdf_finanzas


@login_required(login_url='login')
def dashboard(request):
    mes_str = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    anio, mes = map(int, mes_str.split('-'))

    if request.method == 'POST':
        if 'nueva_categoria' in request.POST:
            crear_categoria_para_usuario(request.user, request.POST['nombre'], request.POST['tipo'])
            messages.success(request, 'Categoría creada')
        elif 'nueva_cuenta' in request.POST:
            crear_cuenta_para_usuario(request.user, request.POST['nombre'])
            messages.success(request, 'Cuenta creada')
        else:
            form = TransaccionForm(request.POST, user=request.user)
            if form.is_valid():
                t = form.save(commit=False)
                t.user = request.user
                t.save()
                messages.success(request, 'Transacción guardada')
        return redirect(f'/?mes={mes_str}')

    # AQUÍ ESTABA EL ERROR: Necesitas recuperar los datos para el contexto
    data = get_dashboard_data(request.user, anio, mes)
    
    context = {
        **data,
        'form': TransaccionForm(user=request.user),
        'mes_actual': mes_str,
        'nombres_categorias': json.dumps([i['categoria__nombre'] for i in data['gastos_data']]),
        'totales_categorias': json.dumps([float(i['total'] or 0) for i in data['gastos_data']]),
    }
    return render(request, 'finanzas/dashboard.html', context)


# Asegúrate de usar login_required en todas las vistas sensibles
@login_required(login_url='login')
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transacciones.csv"'

    writer = csv.writer(response)
    writer.writerow(['Descripcion', 'Monto', 'Fecha', 'Categoria'])

    # CORRECCIÓN: Filtrar por el usuario actual
    transacciones = Transaccion.objects.filter(user=request.user).values_list(
        'descripcion', 'monto', 'fecha', 'categoria__nombre'
    )

    for transaccion in transacciones:
        writer.writerow(transaccion)
    return response

@login_required(login_url='login')
def descargar_reporte_pdf(request):
    mes_seleccionado = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    anio, mes = map(int, mes_seleccionado.split('-'))

    # CORRECCIÓN: Pasar el usuario a calcular_resumen_financiero y filtrar transacciones
    context = {
        'resumen': calcular_resumen_financiero(anio, mes, request.user),
        'transacciones': Transaccion.objects.filter(user=request.user, fecha__year=anio, fecha__month=mes).order_by('-fecha'),
        'mes': mes_seleccionado
    }
    return generar_pdf_finanzas(context)

