
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    secret_key: str = Field(..., alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    database_url: str = Field("sqlite:///./data.db", alias="DATABASE_URL")
    stripe_webhook_secret: str | None = Field(None, alias="STRIPE_WEBHOOK_SECRET")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
