import factory.fuzzy

from fast_zero.models import (
    Category,
    Client,
    Order,
    OrderProduct,
    OrderState,
    Product,
    User,
)


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    descricao = factory.Faker('text')
    valor = factory.fuzzy.FuzzyDecimal(low=1)
    codigo_barras = factory.Faker('text')
    secao = factory.Faker('text')
    estoque_inicial = factory.fuzzy.FuzzyInteger(low=1)
    data_validade = None
    categoria = factory.fuzzy.FuzzyChoice(Category)


class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    state = factory.fuzzy.FuzzyChoice(OrderState)
    client_id = 1


class OrderProductFactory(factory.Factory):
    class Meta:
        model = OrderProduct

    order_id = 1
    product_id = 1


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    nome_completo = factory.Faker('text')
    cpf = factory.Faker('text')
    email = factory.Faker('email')


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
