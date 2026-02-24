# finanzas/tests/test_views.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_dashboard_access_authenticated(auth_client):
    """Prueba que un usuario logueado vea el dashboard con código 200."""
    response = auth_client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert 'Dashboard de Finanzas' in response.content.decode()

@pytest.mark.django_db
def test_dashboard_redirect_unauthenticated(api_client):
    """Prueba que un usuario NO logueado sea redirigido al login (302)."""
    response = api_client.get(reverse('dashboard'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

