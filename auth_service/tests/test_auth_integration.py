# Интеграционные тесты Auth Service через HTTP

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_login_me(client: AsyncClient):
    """Полный поток: регистрация → логин → /auth/me."""
    # Регистрация
    resp = await client.post("/auth/register", json={"email": "komarov@email.com", "password": "secret123"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "komarov@email.com"
    assert "id" in data
    assert "password_hash" not in data

    # Логин
    resp = await client.post(
        "/auth/login",
        data={"username": "komarov@email.com", "password": "secret123"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token

    # /auth/me
    resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    me = resp.json()
    assert me["email"] == "komarov@email.com"


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient):
    """Повторная регистрация с тем же email → 409."""
    payload = {"email": "dup@email.com", "password": "secret123"}
    resp1 = await client.post("/auth/register", json=payload)
    assert resp1.status_code == 201

    resp2 = await client.post("/auth/register", json=payload)
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Логин с неверным паролем → 401."""
    await client.post("/auth/register", json={"email": "wrong@email.com", "password": "secret123"})

    resp = await client.post(
        "/auth/login",
        data={"username": "wrong@email.com", "password": "badpassword"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_no_token(client: AsyncClient):
    """Запрос /auth/me без токена → 401."""
    resp = await client.get("/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_invalid_token(client: AsyncClient):
    """Запрос /auth/me с мусорным токеном → 401."""
    resp = await client.get("/auth/me", headers={"Authorization": "Bearer garbage.token.here"})
    assert resp.status_code == 401
