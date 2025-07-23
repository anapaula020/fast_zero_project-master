from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
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
        'id': 1,
    }


def test_update_user(client):
    # Cria o usuário antes de atualizar
    response_create = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )
    assert response_create.status_code == HTTPStatus.CREATED

    # Agora faz o update no usuário criado (id=1)
    response_update = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response_update.status_code == HTTPStatus.OK
    assert response_update.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client):
    # Cria usuário para garantir que exista antes de deletar
    response_create = client.post(
        '/users/',
        json={
            'username': 'charlie',
            'email': 'charlie@example.com',
            'password': 'password123',
        },
    )
    assert response_create.status_code == HTTPStatus.CREATED

    # Deleta usuário criado (id=1, assumindo sempre o primeiro)
    response_delete = client.delete('/users/1')
    assert response_delete.status_code == HTTPStatus.OK
    assert response_delete.json() == {'message': 'User deleted'}
