import pytest
from app import app, categories

@pytest.fixture
def client():
    # Puts Flask into testing mode so it throws clearer errors
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear out any data before each individual test runs
        categories.clear()
        yield client

def test_create_category_success(client):
    response = client.post('/api/categories', json={"name": "School Work"})
    assert response.status_code == 201
    assert response.json['name'] == "School Work"

def test_create_category_missing_name(client):
    response = client.post('/api/categories', json={})
    assert response.status_code == 400
    assert "error" in response.json

def test_get_all_categories(client):
    client.post('/api/categories', json={"name": "Personal Tasks"})
    response = client.get('/api/categories')
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_single_category_success(client):
    res = client.post('/api/categories', json={"name": "Work"})
    cat_id = res.json['id']
    response = client.get(f'/api/categories/{cat_id}')
    assert response.status_code == 200
    assert response.json['name'] == "Work"

def test_get_single_category_not_found(client):
    response = client.get('/api/categories/999')
    assert response.status_code == 404

def test_update_category_success(client):
    res = client.post('/api/categories', json={"name": "Chores"})
    cat_id = res.json['id']
    response = client.put(f'/api/categories/{cat_id}', json={"name": "Urgent Chores"})
    assert response.status_code == 200
    assert response.json['name'] == "Urgent Chores"

def test_delete_category_success(client):
    res = client.post('/api/categories', json={"name": "Temporary"})
    cat_id = res.json['id']
    response = client.delete(f'/api/categories/{cat_id}')
    assert response.status_code == 200
    
    check_response = client.get(f'/api/categories/{cat_id}')
    assert check_response.status_code == 404