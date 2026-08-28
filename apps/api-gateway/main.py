import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

EXERCISES_SERVICE_URL = os.getenv("EXERCISES_SERVICE_URL", "http://localhost:8001")
STATS_SERVICE_URL = os.getenv("STATS_SERVICE_URL", "http://localhost:8002")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = httpx.AsyncClient()
    yield
    await client.aclose()


app = FastAPI(title="PianOps API Gateway", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


async def proxy(request: Request, target_base: str, path: str) -> Response:
    url = f"{target_base}/{path}"
    body = await request.body()

    upstream_response = await client.request(
        method=request.method,
        url=url,
        params=request.query_params,
        content=body,
        headers={"content-type": request.headers.get("content-type", "application/json")},
    )

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        media_type=upstream_response.headers.get("content-type"),
    )


@app.api_route("/api/exercises/{path:path}", methods=["GET", "POST"])
async def proxy_exercises(request: Request, path: str):
    return await proxy(request, EXERCISES_SERVICE_URL, path)


@app.api_route("/api/stats/{path:path}", methods=["GET", "POST"])
async def proxy_stats(request: Request, path: str):
    return await proxy(request, STATS_SERVICE_URL, path)