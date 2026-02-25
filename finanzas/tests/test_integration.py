# finanzas/tests/test_integration.py
import pytest
from finanzas.tests.factories import TransaccionFactory
from django.urls import reverse

@pytest.fixture
def transactions_batch(authenticated_user):
    """Fixture dinámico: crea N transacciones para un usuario específico."""
    def _create_batch(n):
        return [TransaccionFactory(user=authenticated_user) for _ in range(n)]
    return _create_batch

@pytest.mark.django_db
def test_dashboard_with_many_transactions(auth_client, transactions_batch):
    """Verifica que el dashboard maneje bien un lote de datos."""
    transactions_batch(10)  # Creamos 10 transacciones
    response = auth_client.get(reverse('dashboard'))
    
    # Verificamos que el contexto contenga las 10 transacciones
    assert len(response.context['transacciones']) == 10

