import pytest
from api_app import init_app

@pytest.fixture
async def cli(aiohttp_client):
    app = await init_app()
    client = await aiohttp_client(app)
    return client

@pytest.fixture(scope='module')
def shared_data():
    return {}

@pytest.mark.asyncio
async def test_create_user(cli, shared_data):
    client = await cli
    resp = await client.post('/apiuser', json={
        'name': 'user1',
        'email': 'apiuser@gmail.com',
        'password': 'password',
    })
    assert resp.status == 200
    data = await resp.json()
    shared_data['user_id'] = data['id']
    assert 'id' in data

@pytest.mark.asyncio
async def test_create_location(cli, shared_data):
    client = await cli
    resp = await client.post('/location', json={
        'name': 'sumy',
    })
    assert resp.status == 200
    data = await resp.json()
    shared_data['location_id'] = data['id']
    assert 'id' in data


@pytest.mark.asyncio
async def test_create_device(cli, shared_data):
    client = await cli
    resp = await client.post('/device', json={
        'name': 'Device1',
        'type': 'Type1',
        'login': 'login',
        'password': 'password',
        'location_id': shared_data['location_id'],
        'api_user_id': shared_data['user_id']
    })
    assert resp.status == 200
    data = await resp.json()
    shared_data['id'] = data['id']
    assert 'id' in data

@pytest.mark.asyncio
async def test_get_devices(cli):
    client = await cli
    resp = await client.get('/device')
    assert resp.status == 200
    data = await resp.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_update_device(cli, shared_data):
    client = await cli
    resp = await client.put(f'/device/{shared_data['id']}', json={
        'name': 'NotDevice1',
        'type': 'NotType1',
        'login': 'login',
        'password': 'password',
        'location_id': shared_data['location_id'],
        'api_user_id': shared_data['user_id']
    })
    assert resp.status == 200
    resp = await client.get(f'/device/{shared_data["id"]}')
    data = await resp.json()
    assert data['name'] == 'NotDevice1'

@pytest.mark.asyncio
async def test_delete_device(cli, shared_data):
    client = await cli
    resp = await client.delete(f'/device/{shared_data['id']}')
    assert resp.status == 200
    data = await resp.json()
    assert f"Device {shared_data['id']} status: " in data

@pytest.mark.asyncio
async def test_delete_location(cli, shared_data):
    client = await cli
    resp = await client.delete(f'/location/{shared_data['location_id']}')
    assert resp.status == 200
    data = await resp.json()
    assert f'Location {shared_data["location_id"]} status: ' in data

@pytest.mark.asyncio
async def test_delete_user(cli, shared_data):
    client = await cli
    resp = await client.delete(f'/apiuser/{shared_data['user_id']}')
    assert resp.status == 200
    data = await resp.json()
    assert f'Apiuser {shared_data['user_id']} status: ' in data



