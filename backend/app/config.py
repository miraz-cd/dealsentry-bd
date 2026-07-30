from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "DealSentry BD"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./dealsentry.db"
    SCRAPE_DELAY_SECONDS: int = 2
    CACHE_TTL_HOURS: int = 4
    DARAZ_BASE_URL: str = "https://www.daraz.com.bd"
    PICKABOO_BASE_URL: str = "https://www.pickaboo.com"
    CHALDAL_BASE_URL: str = "https://chaldal.com"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
