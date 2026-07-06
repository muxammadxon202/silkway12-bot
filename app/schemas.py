from pydantic import BaseModel, Field, field_validator, model_validator

from .pricing import SERVICES


class OrderIn(BaseModel):
    """Заявка с сайта. Всё строго валидируется — фронту не доверяем."""

    service: str
    options: list[str] = Field(default_factory=list, max_length=20)
    urgent: bool = False
    # Необязательный контакт клиента (телефон / @username). Ограничен по длине.
    contact: str | None = Field(default=None, max_length=120)
    # Honeypot: скрытое поле на сайте. Люди его не видят, боты-спамеры заполняют.
    # Если пришло непустым — заявка отбрасывается.
    website: str | None = Field(default=None, max_length=200)

    @field_validator("service")
    @classmethod
    def known_service(cls, v: str) -> str:
        if v not in SERVICES:
            raise ValueError("unknown service")
        return v

    @model_validator(mode="after")
    def known_options(self):
        allowed = SERVICES[self.service]["options"]
        # dedup + отбрасываем опции не из белого списка этой услуги
        self.options = [o for o in dict.fromkeys(self.options) if o in allowed]
        return self


class OrderOut(BaseModel):
    ok: bool = True
    id: int | None = None
    price: int
    days: int
