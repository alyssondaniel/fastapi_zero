from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(clientHttp, token_admin):
    response = clientHttp.post(
        '/users',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 2,
    }


def test_create_user_exists_username(clientHttp, user, token_admin):
    response = clientHttp.post(
        '/users',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_exists_email(clientHttp, user, token_admin):
    response = clientHttp.post(
        '/users',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'username': 'alice',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_list_users(clientHttp, token_admin):
    response = clientHttp.get(
        '/users',
        headers={'Authorization': f'Bearer {token_admin}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users_with_users(clientHttp, user, token_admin):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = clientHttp.get(
        '/users/',
        headers={'Authorization': f'Bearer {token_admin}'},
    )
    assert response.json() == {'users': [user_schema]}


def test_show_user(clientHttp, user, token_admin):
    response = clientHttp.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_admin}'},
    )
    assert response.json() == {
        'id': user.id,
        'email': user.email,
        'username': user.username,
    }


def test_update_user(clientHttp, user, token_admin):
    response = clientHttp.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    # assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_user_not_found(clientHttp, token_admin):
    response = clientHttp.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(clientHttp, user, token_admin):
    response = clientHttp.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_admin}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(clientHttp, token_admin):
    response = clientHttp.delete(
        '/users/2', headers={'Authorization': f'Bearer {token_admin}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
