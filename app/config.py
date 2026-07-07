from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str
    database_url: str = "postgresql+asyncpg://silkway:silkway@localhost:5432/silkway"
    allowed_origins: str = "*"
    admin_id: int | None = None

    @field_validator("admin_id", mode="before")
    @classmethod
    def _empty_admin_id_to_none(cls, v):
        # В .env ADMIN_ID= обычно пустой (админ назначается через /start).
        # Пустую строку трактуем как None, иначе pydantic падает на int-парсинге.
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return None
        return v

    @property
    def origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


settings = Settings()
