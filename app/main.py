from fastapi import FastAPI

from app.api.router import router as api_router

app = FastAPI(
    title="Backend API",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
