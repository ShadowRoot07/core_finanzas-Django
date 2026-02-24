import pytest
from finanzas.models import Categoria, Cuenta, Transaccion

@pytest.mark.django_db
def test_categoria_str(categoria_factory):
    # Usamos la factoría registrada en conftest.py
    cat = categoria_factory(nombre="Inversiones")
    assert str(cat) == "Inversiones"

@pytest.mark.django_db
def test_transaccion_relaciones(transaccion_factory):
    # La factoría crea usuario, cuenta y categoría automáticamente
    t = transaccion_factory(monto=500)
    assert t.monto == 500
    assert t.user is not None
    assert t.cuenta is not None
    assert t.categoria is not None

