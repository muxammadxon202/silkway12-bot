import logging

from fastapi import APIRouter, Request

from ..bot.notify import notify_admin
from ..db.models import Order
from ..db.session import SessionLocal
from ..limiter import limiter
from ..pricing import calc
from ..schemas import OrderIn, OrderOut

router = APIRouter()
log = logging.getLogger("silkway.api")


@router.post("/api/orders", response_model=OrderOut)
@limiter.limit("10/minute")
async def create_order(request: Request, data: OrderIn) -> OrderOut:
    # Honeypot: скрытое поле заполняют только боты-спамеры.
    # Отвечаем «ок», но заявку не сохраняем и не шлём.
    if data.website:
        ip = request.client.host if request.client else "?"
        log.warning("honeypot triggered from %s", ip)
        return OrderOut(ok=True, price=0, days=0)

    r = calc(data.service, data.options, data.urgent)
    order = Order(
        service=data.service,
        service_name=r["service_name"],
        options=", ".join(r["chosen"]),
        urgent=data.urgent,
        price=r["price"],
        days=r["days"],
        contact=data.contact,
    )
    async with SessionLocal() as s:
        s.add(order)
        await s.commit()
        await s.refresh(order)

    try:
        await notify_admin(order)
    except Exception:
        # заявка уже сохранена — сбой уведомления не должен ронять ответ сайту
        log.exception("failed to notify admin about order #%s", order.id)

    return OrderOut(ok=True, id=order.id, price=order.price, days=order.days)
