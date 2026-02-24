import pytest
from pytest_factoryboy import register
from finanzas.tests.factories import UserFactory, CategoriaFactory, CuentaFactory, TransaccionFactory
from django.contrib.auth.models import User

# Registramos las factorías para que Pytest las reconozca automáticamente como fixtures
register(UserFactory)
register(CategoriaFactory)
register(CuentaFactory)
register(TransaccionFactory)

@pytest.fixture
def api_client():
    """Fixture para obtener el cliente de prueba de Django."""
    from django.test import Client
    return Client()

@pytest.fixture
def authenticated_user(user_factory):
    """Crea un usuario y lo retorna."""
    return user_factory()

@pytest.fixture
def auth_client(api_client, authenticated_user):
    """Crea un cliente, loguea al usuario y lo retorna para usar en los tests."""
    api_client.force_login(authenticated_user)
    # Adjuntamos el usuario al cliente para poder acceder a él en los tests
    api_client.user = authenticated_user
    return api_client

