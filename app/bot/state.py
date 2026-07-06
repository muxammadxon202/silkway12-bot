from ..config import settings
from ..db.models import BotState
from ..db.session import SessionLocal


async def get_admin_id() -> int | None:
    """ID админа: приоритет — из .env, иначе тот, кто первым сделал /start."""
    if settings.admin_id:
        return settings.admin_id
    async with SessionLocal() as s:
        st = await s.get(BotState, 1)
        return st.admin_chat_id if st else None


async def set_admin_id(chat_id: int) -> bool:
    """Назначить админа, если ещё не назначен. True — если назначен впервые."""
    if settings.admin_id:
        return False
    async with SessionLocal() as s:
        st = await s.get(BotState, 1)
        if st is None:
            s.add(BotState(id=1, admin_chat_id=chat_id))
            await s.commit()
            return True
        if st.admin_chat_id is None:
            st.admin_chat_id = chat_id
            await s.commit()
            return True
        return False
