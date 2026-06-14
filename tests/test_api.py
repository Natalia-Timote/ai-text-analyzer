"""
Testes dos endpoints da API (main.py)

Testamos as rotas HTTP, validações e formato de resposta.
Sem mock — a análise é local, então os testes são 100% reais.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_analyze_returns_expected_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/analyze", json={"text": "Python é uma linguagem incrível."})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "sentiment" in data
    assert "sentiment_score" in data
    assert "keywords" in data
    assert "word_count" in data
    assert "char_count" in data

@pytest.mark.asyncio
async def test_analyze_empty_text():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/analyze", json={"text": "  "})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_analyze_text_too_long():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/analyze", json={"text": "a" * 5001})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_analyze_missing_field():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/analyze", json={})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_analyze_word_and_char_count():
    text = "Python é incrível para IA."
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/analyze", json={"text": text})
    data = response.json()
    assert data["word_count"] == len(text.split())
    assert data["char_count"] == len(text)

@pytest.mark.asyncio
async def test_analyze_sentiment_is_valid():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/analyze", json={"text": "Que dia lindo e maravilhoso!"})
    data = response.json()
    assert data["sentiment"] in ["Positivo", "Neutro", "Negativo"]
    assert -1.0 <= data["sentiment_score"] <= 1.0
