from sys import api_version
from fastapi import FastAPI

API_VERSION = "0.1.0"

app = FastAPI(
    title="CINEMA_ERP API",
    description="The API REST to manage your cinema !",
    version=API_VERSION
)


@app.get("/")
async def root():
    return {
        "message": "API online",
        "status": "running",
        "docs": "http://127.0.0.1:8000/docs",
        "version": API_VERSION
        }


@app.get("/healthy")
async def health():
    return {"status": "healthy"}