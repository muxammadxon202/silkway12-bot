FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd -m app && chown -R app:app /app
USER app

# --proxy-headers + --forwarded-allow-ips="*" — без этого uvicorn видит
# только IP контейнера Caddy для всех посетителей, и rate-limit по IP
# (slowapi/get_remote_address) превращается в общий лимит на весь сайт.
# "*" безопасно здесь только потому, что порт 8000 не публикуется наружу —
# единственный, кто может достучаться до uvicorn, это сам Caddy.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--proxy-headers", "--forwarded-allow-ips", "*"]
