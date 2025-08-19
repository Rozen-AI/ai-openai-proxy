# proxy.py
import os
import httpx
from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
PROXY_SECRET = os.environ.get("PROXY_SECRET", "changeme")

@app.post("/v1/chat/completions")
async def proxy_chat(request: Request, authorization: str | None = Header(None)):
    # простая проверка: наш бот должен посылать заголовок Authorization: Bearer <PROXY_SECRET>
    if authorization != f"Bearer {PROXY_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.json()
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post("https://api.openai.com/v1/chat/completions", json=body, headers=headers)
    return resp.json()
