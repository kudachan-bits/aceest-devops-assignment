import pytest
from app import create_app
from services import calorie_target


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


@pytest.mark.parametrize('program,expected', [('FL', 1540), ('MG', 2450), ('BG', 1820)])
def test_calories(program, expected):
    assert calorie_target(70, program) == expected


@pytest.mark.parametrize('weight', [0, -1, 501, True, '70', None, float('nan'), float('inf')])
def test_invalid_weight(weight):
    with pytest.raises(ValueError):
        calorie_target(weight, 'FL')


def test_invalid_program():
    with pytest.raises(ValueError):
        calorie_target(70, 'UNKNOWN')


def test_health_and_index(client):
    assert client.get('/health').json == {'status': 'ok'}
    assert client.get('/').status_code == 200


def test_programs(client):
    assert set(client.get('/programs').json) == {'FL', 'MG', 'BG'}


def test_client_lifecycle(client):
    record = {'name': 'Demo', 'weight': 70, 'program': 'FL'}
    assert client.get('/clients').json == []
    response = client.post('/clients', json=record)
    assert response.status_code == 201
    assert response.json['calories'] == 1540
    assert client.get('/clients/Demo').status_code == 200
    assert len(client.get('/clients').json) == 1
    assert client.post('/clients', json=record).status_code == 409
    progress = client.post('/clients/Demo/progress', json={'adherence': 80})
    assert progress.status_code == 201
    assert progress.json['progress'] == [{'adherence': 80}]


@pytest.mark.parametrize('body', [{}, [], {'name': ''},
    {'name': 'A', 'weight': 70, 'program': []},
    {'name': 'A', 'weight': -2, 'program': 'FL'}])
def test_invalid_client(client, body):
    assert client.post('/clients', json=body).status_code == 400


@pytest.mark.parametrize('adherence', [-1, 101, True, '80', 80.5, None])
def test_invalid_progress(client, adherence):
    client.post('/clients', json={'name': 'A', 'weight': 70, 'program': 'BG'})
    assert client.post('/clients/A/progress', json={'adherence': adherence}).status_code == 400


def test_unknown_client(client):
    assert client.get('/clients/missing').status_code == 404
    assert client.post('/clients/missing/progress', json={'adherence': 80}).status_code == 404


def test_bad_json(client):
    assert client.post('/clients', data='{', content_type='application/json').status_code == 400
    assert client.post('/clients', data='text').status_code == 415
