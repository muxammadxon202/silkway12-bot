#!/usr/bin/env bash
# Silkway bot — установка в одну команду на Ubuntu VPS.
# Запуск:  bash deploy.sh
set -euo pipefail

REPO="https://github.com/muxammadxon202/silkway12-bot.git"
DIR="silkway12-bot"

echo "==> 1/4 Docker"
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
else
  echo "    уже установлен"
fi

echo "==> 2/4 Код"
if [ -d "$DIR/.git" ]; then
  git -C "$DIR" pull --ff-only
else
  git clone "$REPO" "$DIR"
fi
cd "$DIR"

echo "==> 3/4 Настройки (.env)"
if [ ! -f .env ]; then
  cp .env.example .env
  echo
  echo "    Вставь токен бота от @BotFather и нажми Enter:"
  read -r TOK < /dev/tty
  sed -i "s#^BOT_TOKEN=.*#BOT_TOKEN=${TOK}#" .env
  echo "    .env создан (ALLOWED_ORIGINS и API_DOMAIN уже прописаны)."
else
  echo "    .env уже есть — не трогаю."
fi

echo "==> 4/4 Запуск"
docker compose up -d --build

echo
echo "Жду 45 сек, пока Caddy получит HTTPS-сертификат..."
sleep 45
if curl -fsS https://api.silkway12.uz/health >/dev/null 2>&1; then
  echo "✅ API живой: https://api.silkway12.uz/health отвечает."
  echo "   Теперь открой бота в Telegram и отправь /start — станешь админом."
else
  echo "⚠️  Health пока не отвечает. Обычно это DNS ещё не распространился"
  echo "   или сертификат в процессе. Проверь:"
  echo "     docker compose logs -f caddy"
  echo "   и что A-запись api.silkway12.uz указывает на IP этого сервера."
fi
