import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select

from ..db.models import Order
from ..db.session import SessionLocal
from .state import get_admin_id, set_admin_id

router = Router()
log = logging.getLogger("silkway.bot")


@router.message(Command("start"))
async def cmd_start(m: Message) -> None:
    first = await set_admin_id(m.chat.id)
    if first:
        # ID выводится в консоль — как договаривались, берёшь его отсюда.
        log.info("ADMIN назначен. ADMIN_ID = %s", m.chat.id)
        print(f"\n>>> ADMIN_ID = {m.chat.id}  (сохранён в БД, впиши в .env при желании) <<<\n")
        await m.answer("Готово — ты назначен админом. Заявки с сайта будут приходить сюда.\n/orders — последние заявки.")
        return

    if m.chat.id == await get_admin_id():
        await m.answer("Ты админ. Заявки приходят сюда.\n/orders — последние заявки.")
    else:
        await m.answer("Этот бот принимает заявки для студии Silkway Web Company.")


@router.message(Command("orders"))
async def cmd_orders(m: Message) -> None:
    if m.chat.id != await get_admin_id():
        return
    async with SessionLocal() as s:
        rows = (
            await s.execute(select(Order).order_by(Order.id.desc()).limit(10))
        ).scalars().all()
    if not rows:
        await m.answer("Заявок пока нет.")
        return
    lines = []
    for o in rows:
        price = f"{o.price:,}".replace(",", " ")
        lines.append(f"#{o.id} · {o.service_name} · {price} сум · {o.status}")
    await m.answer("Последние заявки:\n" + "\n".join(lines))
