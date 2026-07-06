import html

from ..db.models import Order
from .instance import bot
from .state import get_admin_id


def format_order(o: Order) -> str:
    # service_name и опции — из нашего белого списка (безопасны).
    # contact — ввод пользователя, экранируем для HTML-разметки.
    parts = [
        "🆕 <b>Новая заявка с сайта</b>",
        f"Услуга: <b>{html.escape(o.service_name)}</b>",
    ]
    if o.options:
        parts.append(f"Опции: {html.escape(o.options)}")
    if o.urgent:
        parts.append("⚡ Срочно: да")
    price = f"{o.price:,}".replace(",", " ")
    parts.append(f"Расчёт: <b>{price}</b> сум · срок: {o.days} дн.")
    if o.contact:
        parts.append(f"Контакт: {html.escape(o.contact)}")
    parts.append(f"<i>#{o.id}</i>")
    return "\n".join(parts)


async def notify_admin(order: Order) -> None:
    admin = await get_admin_id()
    if admin is None:
        return
    await bot.send_message(admin, format_order(order))
