from datetime import date
from http import HTTPStatus

from fast_zero.factories import OrderFactory, OrderProductFactory


def test_create_order(clientHttp, token, client, products):
    response = clientHttp.post(
        '/orders/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'state': 'aguardando',
            'client_id': client.id,
            'product_ids': [product.id for product in products],
        },
    )

    assert response.json() == {
        'id': 1,
        'state': 'aguardando',
        'client_id': client.id,
    }


def test_list_orders_should_return_5_orders(session, clientHttp, client, token):
    expected_orders = 5
    session.bulk_save_objects(
        OrderFactory.create_batch(
            expected_orders,
            client_id=client.id,
        )
    )
    session.commit()

    response = clientHttp.get(
        '/orders/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['orders']) == expected_orders


def test_list_orders_pagination_should_return_2_orders(
    session, client, clientHttp, token
):
    expected_orders = 2
    session.bulk_save_objects(OrderFactory.create_batch(5, client_id=client.id))
    session.commit()

    response = clientHttp.get(
        '/orders/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['orders']) == expected_orders


def test_list_orders_filter_arrange_date_should_return_5_orders(
    session, client, clientHttp, token
):
    expected_orders = 5
    session.bulk_save_objects(
        OrderFactory.create_batch(expected_orders, client_id=client.id)
    )
    session.commit()

    date_end = date.today().strftime('%Y-%m-%d')
    response = clientHttp.get(
        f'/orders/?created_start=2024-06-01&created_end={date_end}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['orders']) == expected_orders


def test_list_orders_filter_product_secao_should_return_1_orders(
    session, clientHttp, token, product, order
):
    expected_orders = 1
    session.bulk_save_objects(
        OrderProductFactory.create_batch(
            1, order_id=order.id, product_id=product.id
        )
    )
    session.commit()

    response = clientHttp.get(
        '/orders/?product_secao=alimentacao',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['orders']) == expected_orders


def test_list_orders_filter_order_id_should_return_1_orders(
    clientHttp, token, order
):
    expected_orders = 1

    response = clientHttp.get(
        f'/orders/?order_id={order.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['orders']) == expected_orders


def test_list_orders_filter_status_should_return_5_orders(
    session, clientHttp, token, client
):
    expected_orders = 5
    session.bulk_save_objects(
        OrderFactory.create_batch(
            expected_orders, state='pago', client_id=client.id
        )
    )
    session.commit()

    response = clientHttp.get(
        '/orders/?state=pago',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['orders']) == expected_orders


def test_list_orders_filter_client_should_return_5_orders(
    session, clientHttp, token, client
):
    expected_orders = 5
    session.bulk_save_objects(
        OrderFactory.create_batch(expected_orders, client_id=client.id)
    )
    session.commit()

    response = clientHttp.get(
        f'/orders/?client_id={client.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['orders']) == expected_orders


def test_show_order(clientHttp, token, order):
    response = clientHttp.get(
        f'/orders/{order.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {
        'id': order.id,
        'state': order.state,
        'client_id': order.client_id,
    }


def test_patch_order_error(clientHttp, token, client, products):
    response = clientHttp.patch(
        '/orders/10',
        json={
            'state': 'pago',
            'client_id': client.id,
            'product_ids': [product.id for product in products],
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Order not found.'}


def test_patch_order(session, clientHttp, client, token):
    order = OrderFactory(client_id=client.id)

    session.add(order)
    session.commit()

    response = clientHttp.patch(
        f'/orders/{order.id}',
        json={
            'state': 'pago',
            'client_id': client.id,
            'product_ids': [],
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['state'] == 'pago'


def test_delete_order(session, clientHttp, client, token):
    order = OrderFactory(client_id=client.id)

    session.add(order)
    session.commit()

    response = clientHttp.delete(
        f'/orders/{order.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Order has been deleted successfully.'
    }


def test_delete_order_error(clientHttp, token):
    response = clientHttp.delete(
        '/orders/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Order not found.'}
