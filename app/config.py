from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str
    database_url: str = "postgresql+asyncpg://silkway:silkway@localhost:5432/silkway"
    # Без дефолта "*" — если .env потеряется/разъедется, CORS должен закрыться,
    # а не открыться всем.
    allowed_origins: str = ""
    # Обязателен: без известного ID заранее первый написавший /start становился
    # бы админом и перехватывал бы все заявки с сайта. Падаем на старте, если
    # не задан, а не тихо открываем окно захвата.
    admin_id: int

    @property
    def origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


settings = Settings()
