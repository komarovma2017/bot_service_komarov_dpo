# Клиент OpenRouter — вызов LLM через httpx

import httpx

from app.core.config import settings


async def call_openrouter(prompt: str) -> str:
    """Отправляет запрос к OpenRouter и возвращает текст ответа."""
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": settings.OPENROUTER_SITE_URL,
        "X-Title": settings.OPENROUTER_APP_NAME,
    }
    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        )

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter вернул статус {response.status_code}: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]
