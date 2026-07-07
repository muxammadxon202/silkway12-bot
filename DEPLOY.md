# Деплой Silkway Bot на VPS (Docker + Caddy, авто-HTTPS)

Пошагово. Сайт живёт на HTTPS (GitHub Pages), поэтому бот тоже должен быть на
HTTPS-домене — за это отвечает Caddy, он сам получает сертификат Let's Encrypt.

Итог: API будет доступен по `https://api.silkway12.uz/api/orders`, заявки с сайта
пойдут напрямую в Telegram админу.

---

## 0. Что нужно заранее

- VPS с Ubuntu 22.04+ и root/sudo доступом, знаешь его IP.
- Домен `silkway12.uz` (есть).
- Токен бота от [@BotFather](https://t.me/BotFather).

## 1. DNS: направить поддомен на сервер

В панели управления доменом добавь **A-запись**:

```
Тип: A   Имя: api   Значение: <IP_твоего_VPS>   TTL: авто
```

Проверить (подожди 5–30 мин на распространение):

```bash
nslookup api.silkway12.uz     # должен вернуть твой IP
```

> Если сайт тоже хочешь на `silkway12.uz` (вместо github.io) — это отдельный шаг
> через GitHub Pages custom domain, скажи, распишу. Для работы заявок он не нужен.

## 2. Установить Docker на VPS

```bash
ssh root@<IP_VPS>
curl -fsSL https://get.docker.com | sh
```

## 3. Забрать код бота

```bash
git clone https://github.com/muxammadxon202/silkway12-bot.git
cd silkway12-bot
cp .env.example .env
nano .env
```

Заполни в `.env`:

```
BOT_TOKEN=<токен от @BotFather>
ALLOWED_ORIGINS=https://muxammadxon202.github.io,https://silkway12.uz,https://www.silkway12.uz
API_DOMAIN=api.silkway12.uz
# DATABASE_URL и ADMIN_ID можно не трогать
```

> `BOT_TOKEN` держи только здесь. В git `.env` не попадает (см. `.gitignore`).

## 4. Запустить

```bash
docker compose up -d --build
docker compose logs -f
```

Caddy 30–60 сек получает сертификат. Проверь здоровье:

```bash
curl https://api.silkway12.uz/health      # {"ok":true}
```

## 5. Стать админом бота

Открой бота в Telegram, отправь `/start`. Первый написавший становится админом,
его ID появится в логах. По желанию впиши `ADMIN_ID` в `.env` и `docker compose up -d`.

Проверь заявку боевым запросом:

```bash
curl -X POST https://api.silkway12.uz/api/orders \
  -H "Content-Type: application/json" \
  -d '{"service":"landing","options":["anim"],"urgent":true,"contact":"@test"}'
```

Тебе в Telegram должно прийти сообщение с заявкой.

## 6. Включить отправку с сайта

В репозитории **сайта** (`silkway12`) открой `js/main.js`, найди вверху:

```js
const ORDER_API = "";
```

Впиши домен и запушь:

```js
const ORDER_API = "https://api.silkway12.uz";
```

```bash
git add js/main.js && git commit -m "Подключение сайта к боту" && git push
```

Через минуту GitHub Pages обновится — кнопка «Отправить заявку» будет слать заказ
прямо в Telegram. Если бот вдруг недоступен, сайт сам откатится на копирование в
буфер + открытие чата (заявка не потеряется).

## Обслуживание

```bash
docker compose logs -f app       # логи бота/API
docker compose logs -f caddy     # логи сертификата
docker compose pull && docker compose up -d --build   # обновить после git pull
docker compose down              # остановить
```

Заявки хранятся в PostgreSQL (том `pgdata`), команда бота `/orders` — последние 10.
