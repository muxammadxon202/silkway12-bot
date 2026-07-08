import re

from pydantic import BaseModel, Field, field_validator, model_validator

from .pricing import SERVICES

# Простая проверка формата email — без внешней зависимости email-validator.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class OrderIn(BaseModel):
    """Заявка с сайта. Всё строго валидируется — фронту не доверяем."""

    service: str
    options: list[str] = Field(default_factory=list, max_length=20)
    urgent: bool = False
    # Телефон / @username — обязателен, иначе некуда перезвонить клиенту.
    contact: str = Field(min_length=1, max_length=120)
    # Необязательный email — дополнительный способ связи.
    email: str | None = Field(default=None, max_length=160)
    # Honeypot: скрытое поле на сайте. Люди его не видят, боты-спамеры заполняют.
    # Если пришло непустым — заявка отбрасывается.
    website: str | None = Field(default=None, max_length=200)

    @field_validator("contact")
    @classmethod
    def contact_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("contact is required")
        return v

    @field_validator("email")
    @classmethod
    def email_format(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if not _EMAIL_RE.match(v):
            raise ValueError("invalid email format")
        return v

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
    days_text: str = ""
