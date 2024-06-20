from http import HTTPStatus

from fast_zero.factories import ClientFactory


def test_create_client(clientHttp, token_admin):
    response = clientHttp.post(
        '/clients/',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'nome_completo': 'Jhon Doe',
            'cpf': '00011122233',
            'email': 'jhondoe@example.com',
        },
    )
    assert response.json() == {
        'id': 1,
        'nome_completo': 'Jhon Doe',
        'email': 'jhondoe@example.com',
    }


def test_list_clients_should_return_5_clients(session, clientHttp, token):
    expected_clients = 5
    session.bulk_save_objects(ClientFactory.create_batch(5))
    session.commit()

    response = clientHttp.get(
        '/clients/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clients']) == expected_clients


def test_list_clients_pagination_should_return_2_clients(
    session, clientHttp, token
):
    expected_clients = 2
    session.bulk_save_objects(ClientFactory.create_batch(5))
    session.commit()

    response = clientHttp.get(
        '/clients/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clients']) == expected_clients


def test_list_clients_filter_nome_completo_should_return_5_clients(
    session, clientHttp, token
):
    expected_clients = 5
    session.bulk_save_objects(
        ClientFactory.create_batch(5, nome_completo='Maria Jose')
    )
    session.commit()

    response = clientHttp.get(
        '/clients/?nome_completo=Maria Jose',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clients']) == expected_clients


def test_list_clients_filter_cpf_should_return_5_clients(
    session, clientHttp, token
):
    expected_clients = 5
    session.bulk_save_objects(ClientFactory.create_batch(5, cpf='00011122233'))
    session.commit()

    response = clientHttp.get(
        '/clients/?cpf=00011122233',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clients']) == expected_clients


def test_list_clients_filter_email_should_return_5_clients(
    session, clientHttp, token
):
    expected_clients = 1
    session.bulk_save_objects(
        ClientFactory.create_batch(
            expected_clients, email='jhondoe@example.com'
        )
    )
    session.commit()

    response = clientHttp.get(
        '/clients/?email=jhondoe@example.com',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clients']) == expected_clients


def test_list_clients_filter_combined_should_return_5_clients(
    session, clientHttp, token
):
    expected_clients = 8
    session.bulk_save_objects(
        ClientFactory.create_batch(
            5,
            nome_completo='Jose Maria',
            cpf='00011199933',
        )
    )

    session.bulk_save_objects(
        ClientFactory.create_batch(
            3,
            nome_completo='Antonio Jose',
            cpf='99988877766',
        )
    )
    session.commit()

    response = clientHttp.get(
        '/clients/?nome_completo=Jose&cpf=999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clients']) == expected_clients


def test_show_client(clientHttp, client, token):
    response = clientHttp.get(
        f'/clients/{client.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.json() == {
        'id': client.id,
        'nome_completo': client.nome_completo,
        'email': client.email,
    }


def test_update_client_error(clientHttp, token_admin):
    response = clientHttp.put(
        '/clients/10',
        json={'nome_completo': '', 'cpf': '', 'email': ''},
        headers={'Authorization': f'Bearer {token_admin}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Client not found.'}


def test_update_client(session, clientHttp, token_admin):
    client = ClientFactory()

    session.add(client)
    session.commit()

    response = clientHttp.put(
        f'/clients/{client.id}',
        json={
            'nome_completo': 'Joaquim da Silva',
            'cpf': '12345678900',
            'email': 'jquimsilva@example.com',
        },
        headers={'Authorization': f'Bearer {token_admin}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['nome_completo'] == 'Joaquim da Silva'


def test_delete_client(session, clientHttp, token_admin):
    client = ClientFactory()

    session.add(client)
    session.commit()

    response = clientHttp.delete(
        f'/clients/{client.id}',
        headers={'Authorization': f'Bearer {token_admin}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Client has been deleted successfully.'
    }


def test_delete_client_error(clientHttp, token_admin):
    response = clientHttp.delete(
        f'/clients/{10}', headers={'Authorization': f'Bearer {token_admin}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Client not found.'}
