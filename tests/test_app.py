from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_get_root_path_and_return_ok_and_hello_world_json():
    client = TestClient(app)
    reponse = client.get('/')
    assert reponse.status_code == HTTPStatus.OK
    assert reponse.json() == {'message': 'Olá Mundo!'}
