# KLM V2.2 Backend - Entry Point
# Multi-Agent RAG System for Khmer Language Learning

from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="KLM V2.2 API",
    description="Multi-Agent RAG System for Khmer Language Learning",
    version="2.2.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.2.0"}


@app.get("/")
async def root():
    return {
        "project": "KLM V2.2",
        "status": "ready",
        "next_step": "Begin ingestion workflow coding",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
