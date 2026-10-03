from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Persynta API"
    debug: bool = True

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    frontend_url: str = "http://localhost:3000"

    encryption_key: str
    database_url: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    email_provider: str = "console"
    email_from: str = "no-reply@persynta.local"
    email_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()