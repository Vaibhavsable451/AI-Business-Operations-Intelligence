from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./business_ops.db"
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
