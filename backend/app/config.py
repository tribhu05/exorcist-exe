import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "PHANTOM//SHELL"
    APP_VERSION: str = "1.0.0"
    TAGLINE: str = "The Ghost in your Terminal. Local. Offline. Omnipresent."
    
    # Open-weight local LLM configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "gemma2:2b")
    OLLAMA_TIMEOUT_SECONDS: float = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "35.0"))
    ENABLE_OFFLINE_FALLBACK: bool = os.getenv("ENABLE_OFFLINE_FALLBACK", "true").lower() in ("true", "1", "yes")
    
    # Storage
    DB_PATH: str = os.getenv("PHANTOM_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "phantom_grimoire.db"))
    
    # API Host
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()
