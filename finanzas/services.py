from django.db.models import Sum
from .models import Transaccion

def get_saldo_total(user):
    """Suma total de ingresos menos gastos para un usuario específico."""
    ingresos = Transaccion.objects.filter(user=user, categoria__tipo='I').aggregate(Sum('monto'))['monto__sum'] or 0
    gastos = Transaccion.objects.filter(user=user, categoria__tipo='G').aggregate(Sum('monto'))['monto__sum'] or 0
    return ingresos - gastos

def get_gastos_por_categoria(user):
    """Gastos agrupados por categoría para un usuario específico."""
    return Transaccion.objects.filter(user=user, categoria__tipo='G') \
        .values('categoria__nombre') \
        .annotate(total=Sum('monto')) \
        .order_by('-total')

def calcular_resumen_financiero(anio, mes, user):
    """Retorna ingresos, gastos y saldo neto para un usuario y periodo específico."""
    transacciones = Transaccion.objects.filter(user=user, fecha__year=anio, fecha__month=mes)
    totales = transacciones.values('categoria__tipo').annotate(total=Sum('monto'))
    
    resumen = {'ingresos': 0, 'gastos': 0}
    for item in totales:
        if item['categoria__tipo'] == 'I':
            resumen['ingresos'] = item['total'] or 0
        else:
            resumen['gastos'] = item['total'] or 0

    resumen['saldo_neto'] = resumen['ingresos'] - resumen['gastos']
    return resumen

