import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_dashboard_requiere_login(client):
    # Intentamos acceder al dashboard sin estar logueados
    url = reverse('nombre_de_tu_ruta_dashboard')
    response = client.get(url)
    
    # Debería redirigirnos al login (código 302)
    assert response.status_code == 302
    assert '/login/' in response.url

