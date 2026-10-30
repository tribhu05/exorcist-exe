from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import autopsy, exorcist, terminal, grimoire, game

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="EXORCIST.EXE // PHANTOM - An autonomous offline-first AI Cyber-Noir Detective & Terminal Game for Hacktoberfest 2026 Week 4."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game.router)
app.include_router(terminal.router)
app.include_router(autopsy.router)
app.include_router(exorcist.router)
app.include_router(grimoire.router)

@app.get("/")
async def root():
    return {
        "spectre": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "watching",
        "tagline": settings.TAGLINE,
        "model": settings.OLLAMA_MODEL,
        "airgap_mode": "100% OFFLINE SECURE"
    }

@app.get("/healthz")
async def healthz():
    return {"status": "alive", "telemetry_egress": 0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
