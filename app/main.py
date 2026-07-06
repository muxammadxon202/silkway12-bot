import asyncio
import contextlib
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .api.orders import router as api_router
from .bot.handlers import router as bot_router
from .bot.instance import bot, dp
from .config import settings
from .db.session import init_db
from .limiter import limiter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("silkway")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    dp.include_router(bot_router)
    await bot.delete_webhook(drop_pending_updates=True)
    # polling бота крутится в фоне рядом с API-сервером
    polling = asyncio.create_task(dp.start_polling(bot, handle_signals=False))
    log.info("Bot polling started. Отправь боту /start, чтобы стать админом.")
    try:
        yield
    finally:
        polling.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await polling
        await bot.session.close()


app = FastAPI(title="Silkway Bot Backend", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"ok": True}
