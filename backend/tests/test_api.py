import pytest
import asyncio
from httpx import AsyncClient
from server import app
import os

os.environ['MONGO_URL'] = 'mongodb://localhost:27017'
os.environ['DB_NAME'] = 'test_database'
os.environ['CORS_ORIGINS'] = '*'

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/api/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "active"

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test User",
            "preferences": {}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_get_movies(client):
    response = await client.get("/api/movies?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "movies" in data
    assert "total" in data
