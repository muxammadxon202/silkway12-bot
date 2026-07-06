# Silkway Bot Backend

Бэкенд для сайта [Silkway Web Company](https://github.com/muxammadxon202/silkway12).
Принимает заявки с сайта (`POST /api/orders`), сохраняет их в PostgreSQL и
пересылает админу в Telegram. Бот и API работают в одном процессе.

- **Стек:** Python · aiogram 3 · FastAPI · SQLAlchemy (async) · PostgreSQL
- **Режим бота:** long polling (webhook можно добавить позже)

## Архитектура

```
Сайт  --POST /api/orders-->  FastAPI  --> валидация (Pydantic)
                                       --> пересчёт цены (pricing.py)
                                       --> запись в PostgreSQL
                                       --> aiogram: сообщение админу
```

Цена **всегда** считается на бэкенде (`app/pricing.py`) — числу с сайта не доверяем.

## Безопасность

- `BOT_TOKEN` и `ADMIN_ID` — только в `.env` (в git не коммитятся).
- Валидация услуги/опций по белому списку, honeypot-поле `website` против спам-ботов.
- Rate-limit: 10 заявок/мин и 60/час с одного IP.
- CORS: заявки принимаются только с домена(ов) из `ALLOWED_ORIGINS`.

## Запуск на VPS (Docker)

```bash
git clone <этот-репозиторий> silkway12-bot && cd silkway12-bot
cp .env.example .env
nano .env          # впиши BOT_TOKEN, ALLOWED_ORIGINS (домен сайта)
docker compose up -d --build
docker compose logs -f app
```

Затем в Telegram отправь боту `/start` — ты станешь админом, а твой
`ADMIN_ID` появится в логах (`docker compose logs app`). При желании впиши
его в `.env` как `ADMIN_ID` и перезапусти (`docker compose up -d`).

## Локальный запуск (без Docker)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # укажи локальный DATABASE_URL и BOT_TOKEN
uvicorn app.main:app --reload
```

## Команды бота

- `/start` — назначить себя админом (первый запустивший) / проверить статус
- `/orders` — последние 10 заявок (только админу)

## Подключение сайта (следующий шаг)

Кнопка «Отправить заявку» на сайте сейчас копирует текст в буфер. Чтобы
слать напрямую, замените обработчик на `fetch`:

```js
await fetch("https://<ваш-домен-или-ip>:8000/api/orders", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    service: state.service,
    options: [...state.options],
    urgent: state.urgent,
    contact: "",     // телефон/@username, если добавите поле
    website: "",     // honeypot — оставить пустым
  }),
});
```

Endpoint пересчитает цену сам и вернёт `{ ok, id, price, days }`.

## Структура

```
app/
  main.py         FastAPI + запуск polling
  config.py       чтение .env
  pricing.py      услуги/цены (зеркало js/main.js) + calc()
  schemas.py      Pydantic-валидация заявки + honeypot
  limiter.py      rate-limit
  api/orders.py   POST /api/orders
  bot/instance.py Bot + Dispatcher
  bot/handlers.py /start (ловит admin_id), /orders
  bot/state.py    хранение admin_id
  bot/notify.py   заявка -> сообщение
  db/models.py    Order, BotState
  db/session.py   async engine + init_db
```
