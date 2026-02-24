import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from faker import Faker
from finanzas.models import Categoria, Cuenta, Transaccion

fake = Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda o: fake.email())

class CategoriaFactory(DjangoModelFactory):
    class Meta:
        model = Categoria
    
    user = factory.SubFactory(UserFactory)
    nombre = factory.LazyAttribute(lambda o: fake.word())
    tipo = 'G' # Por defecto Gasto

class CuentaFactory(DjangoModelFactory):
    class Meta:
        model = Cuenta
    
    user = factory.SubFactory(UserFactory)
    nombre = factory.LazyAttribute(lambda o: fake.word())

class TransaccionFactory(DjangoModelFactory):
    class Meta:
        model = Transaccion
    
    user = factory.SubFactory(UserFactory)
    cuenta = factory.SubFactory(CuentaFactory)
    categoria = factory.SubFactory(CategoriaFactory)
    monto = factory.LazyAttribute(lambda o: fake.random_int(min=10, max=1000))
    descripcion = factory.LazyAttribute(lambda o: fake.sentence())

