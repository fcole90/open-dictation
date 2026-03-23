from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    HOTKEY: str = "f4"
    MODEL_SIZE: str = "base.en"
    COMPUTE_DEVICE: str = "cpu"


settings = Settings()
