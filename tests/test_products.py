from http import HTTPStatus

from fast_zero.factories import ProductFactory
from fast_zero.models import Category


def test_create_product(clientHttp, token):
    response = clientHttp.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'descricao': 'Tênis AllStar',
            'valor': 123.45,
            'codigo_barras': 'xxxxxxxxxxxxx',
            'secao': 'vestuário',
            'categoria': 'roupas',
            'estoque_inicial': 10,
            'data_validade': None,
        },
    )
    assert response.json() == {
        'id': 1,
        'descricao': 'Tênis AllStar',
        'valor': 123.45,
        'codigo_barras': 'xxxxxxxxxxxxx',
        'secao': 'vestuário',
        'categoria': 'roupas',
        'estoque_inicial': 10,
        'data_validade': None,
    }


def test_list_products_should_return_5_products(session, clientHttp, token):
    expected_products = 5
    session.bulk_save_objects(ProductFactory.create_batch(expected_products))
    session.commit()

    response = clientHttp.get(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['products']) == expected_products


def test_list_products_pagination_should_return_2_products(
    session, clientHttp, token
):
    expected_products = 2
    session.bulk_save_objects(ProductFactory.create_batch(5))
    session.commit()

    response = clientHttp.get(
        f'/products/?offset=1&limit={expected_products}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['products']) == expected_products


def test_list_products_filter_descricao_should_return_5_products(
    session, clientHttp, token
):
    expected_products = 5
    session.bulk_save_objects(
        ProductFactory.create_batch(5, descricao='Test product 1')
    )
    session.commit()

    response = clientHttp.get(
        '/products/?descricao=Test product 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['products']) == expected_products


def test_list_products_filter_categoria_should_return_5_products(
    session, clientHttp, token
):
    expected_products = 5
    session.bulk_save_objects(
        ProductFactory.create_batch(expected_products, categoria=Category.shoes)
    )
    session.commit()

    response = clientHttp.get(
        '/products/?categoria=shoes',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['products']) == expected_products


def test_list_products_filter_valor_should_return_5_products(
    session, clientHttp, token
):
    expected_products = 5
    session.bulk_save_objects(
        ProductFactory.create_batch(expected_products, valor=123.45)
    )
    session.commit()

    response = clientHttp.get(
        '/products/?valor=123.45',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['products']) == expected_products


def test_list_products_filter_disponibilidade_should_return_5_products(
    session, clientHttp, token
):
    expected_products = 1
    session.bulk_save_objects(
        ProductFactory.create_batch(expected_products, estoque_inicial=1)
    )
    session.commit()

    response = clientHttp.get(
        '/products/?disponivel=True',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['products']) > 0


def test_patch_product_error(clientHttp, token):
    response = clientHttp.patch(
        '/products/10',
        json={
            'descricao': 'Tênis AllStar',
            'valor': 45.45,
            'codigo_barras': 'xxxxxxxxxxxxx',
            'secao': 'vestuário',
            'categoria': 'roupas',
            'estoque_inicial': 10,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Product not found.'}


def test_patch_product(session, clientHttp, token):
    product = ProductFactory()

    session.add(product)
    session.commit()

    response = clientHttp.patch(
        f'/products/{product.id}',
        json={
            'descricao': 'Teste1',
            'valor': 123.45,
            'codigo_barras': 'xxxxxxxxxxxxx',
            'secao': 'vestuário',
            'categoria': 'roupas',
            'estoque_inicial': 10,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['descricao'] == 'Teste1'


def test_delete_product(session, clientHttp, token):
    product = ProductFactory()

    session.add(product)
    session.commit()

    response = clientHttp.delete(
        f'/products/{product.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Product has been deleted successfully.'
    }


def test_delete_product_error(clientHttp, token):
    response = clientHttp.delete(
        f'/products/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Product not found.'}
