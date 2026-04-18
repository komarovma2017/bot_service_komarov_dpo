# Интеграционные тесты OpenRouter клиента через respx

import pytest
import respx

from app.services.openrouter_client import call_openrouter


@pytest.mark.asyncio
async def test_call_openrouter_success():
    """Корректный ответ OpenRouter возвращается как текст."""
    fake_response = {
        "choices": [
            {"message": {"content": "Python — язык программирования."}}
        ]
    }

    with respx.mock:
        respx.post("https://openrouter.ai/api/v1/chat/completions").respond(
            status_code=200, json=fake_response
        )
        result = await call_openrouter("Что такое Python?")

    assert result == "Python — язык программирования."


@pytest.mark.asyncio
async def test_call_openrouter_error():
    """Не-200 ответ от OpenRouter вызывает RuntimeError."""
    with respx.mock:
        respx.post("https://openrouter.ai/api/v1/chat/completions").respond(
            status_code=500, text="Internal Server Error"
        )
        with pytest.raises(RuntimeError):
            await call_openrouter("Тест")
