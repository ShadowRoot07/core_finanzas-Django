from django.db.models import Sum
from .models import Transaccion

def get_saldo_total():
    # Suma todos los ingresos y resta los gastos
    # Nota: Aquí asumo que tu categoría tiene un campo 'tipo' ('I' o 'G')
    ingresos = Transaccion.objects.filter(categoria__tipo='I').aggregate(Sum('monto'))['monto__sum'] or 0
    gastos = Transaccion.objects.filter(categoria__tipo='G').aggregate(Sum('monto'))['monto__sum'] or 0
    return ingresos - gastos


def get_gastos_por_categoria():
    # Filtramos solo gastos ('G'), agrupamos por nombre de categoría y sumamos el monto
    return Transaccion.objects.filter(categoria__tipo='G') \
        .values('categoria__nombre') \
        .annotate(total=Sum('monto')) \
        .order_by('-total') # Ordenamos de mayor a menor gasto 


def calcular_resumen_financiero():
    """
    Retorna un diccionario con el saldo total, ingresos y gastos.
    """
    # Utilizamos .aggregate() para que la base de datos haga la suma.
    # Es mucho más rápido que sumar en Python.
    totales = Transaccion.objects.values('categoria__tipo').annotate(total=Sum('monto'))
    
    # Transformamos el resultado para que sea fácil de leer
    resumen = {'ingresos': 0, 'gastos': 0}
    for item in totales:
        if item['categoria__tipo'] == 'I':
            resumen['ingresos'] = item['total'] or 0
        else:
            resumen['gastos'] = item['total'] or 0
            
    resumen['saldo_neto'] = resumen['ingresos'] - resumen['gastos']
    return resumen


