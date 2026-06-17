from fastapi import FastAPI

from app.routers import clients, films, reservations, rooms, seances, tickets

API_VERSION = "0.1.0"

app = FastAPI(
    title="CINEMA_ERP API",
    description="The API REST to manage your cinema !",
    version=API_VERSION
)

app.include_router(films.router)
app.include_router(rooms.router)
app.include_router(seances.router)
app.include_router(clients.router)
app.include_router(reservations.router)
app.include_router(tickets.router)


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