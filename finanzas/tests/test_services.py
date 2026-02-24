import pytest
from finanzas.services import calcular_resumen_financiero
from finanzas.models import Transaccion
from django.utils import timezone

@pytest.mark.django_db
def test_resumen_financiero_calculo(transaccion_factory, user_factory):
    user = user_factory()
    # Creamos un par de transacciones para el usuario
    transaccion_factory(user=user, monto=100, categoria__tipo='I') # Ingreso
    transaccion_factory(user=user, monto=30, categoria__tipo='G')   # Gasto
    
    fecha = timezone.now()
    resumen = calcular_resumen_financiero(fecha.year, fecha.month, user)
    
    assert resumen['ingresos'] == 100
    assert resumen['gastos'] == 30
    assert resumen['saldo_neto'] == 70

@pytest.mark.django_db
def test_servicio_error_fecha():
    # Practicando el uso de 'raises'
    # Si tu servicio espera un formato de fecha específico y recibe basura
    with pytest.raises(ValueError):
        # Simulación de llamada incorrecta
        calcular_resumen_financiero("año", "mes", None)

