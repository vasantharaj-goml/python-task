from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Service Desk"
    app_version: str = "1.0.0"
    debug: bool = True

    database_url: str
    database_ready: bool = True

    aws_demo_mode: bool = False
    aws_region: str = "us-east-1"
    bedrock_model_id: str

    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_session_token: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()