"""Зеркало SERVICES из фронтенда (js/main.js).

Цена и срок ВСЕГДА считаются здесь, на бэкенде. Числу, пришедшему
с сайта, не доверяем — иначе клиент подделает сумму заявки.
Держи в синхроне с js/main.js при изменении цен/опций.
"""
import math

SERVICES = {
    "landing": {
        "name": "Лендинг",
        "base": 2500000,
        "days": 5,
        "options": {
            "anim": {"name": "Анимации и микро-взаимодействия", "price": 300000},
            "lang2": {"name": "Вторая языковая версия (UZ или RU)", "price": 400000},
            "pay": {"name": "Приём оплаты Click / Payme", "price": 500000},
            "seo": {"name": "SEO-база и подключение аналитики", "price": 250000},
            "host": {"name": "Хостинг и домен .uz на год", "price": 700000},
        },
    },
    "site": {
        "name": "Сайт компании",
        "base": 4500000,
        "days": 10,
        "options": {
            "admin": {"name": "Админ-панель — сами меняете контент", "price": 1500000},
            "blog": {"name": "Раздел новостей или блога", "price": 500000},
            "lang2": {"name": "Вторая языковая версия (UZ или RU)", "price": 600000},
            "tg": {"name": "Заявки с сайта в Telegram", "price": 400000},
            "crm": {"name": "Интеграция с CRM", "price": 2500000},
            "host": {"name": "Хостинг и домен .uz на год", "price": 700000},
        },
    },
    "bot": {
        "name": "Telegram-бот",
        "base": 2500000,
        "days": 7,
        "options": {
            "pay": {"name": "Приём платежей в боте", "price": 700000},
            "admin": {"name": "Админ-панель для управления ботом", "price": 800000},
            "mail": {"name": "Рассылки по базе клиентов", "price": 400000},
            "site": {"name": "Интеграция с вашим сайтом", "price": 500000},
            "host": {"name": "Сервер и работа бота на год", "price": 600000},
        },
    },
    "wedding": {
        "name": "Свадебное приглашение",
        "base": 800000,
        "days": 3,
        "options": {
            "guests": {"name": "Личные ссылки для каждого гостя", "price": 200000},
            "rsvp": {"name": "Ответы гостей вам в Telegram", "price": 150000},
            "music": {"name": "Музыка и анимация открытия", "price": 150000},
            "map": {"name": "Карта и маршрут до зала", "price": 100000},
        },
    },
    "shop": {
        "name": "Интернет-магазин",
        "base": 7000000,
        "days": 14,
        "options": {
            "pay": {"name": "Оплата Click / Payme", "price": 800000},
            "stock": {"name": "Учёт склада и остатков", "price": 1000000},
            "bot": {"name": "Telegram-бот магазина", "price": 1200000},
            "delivery": {"name": "Доставка и статусы заказов", "price": 600000},
            "crm": {"name": "Интеграция с CRM и складом", "price": 2500000},
            "host": {"name": "Хостинг и домен .uz на год", "price": 700000},
        },
    },
    "optim": {
        "name": "Оптимизация бизнес-процессов",
        "base": 6000000,
        "days": 14,
        "options": {
            "audit": {"name": "Глубокий аудит отделов", "price": 1500000},
            "docs": {"name": "Регламенты и инструкции", "price": 800000},
            "auto": {"name": "Автоматизация одного процесса", "price": 1200000},
        },
    },
    "hr": {
        "name": "HR-интеграция",
        "base": 7000000,
        "days": 16,
        "options": {
            "ats": {"name": "Трекер кандидатов (ATS)", "price": 1500000},
            "bot": {"name": "HR-бот в Telegram", "price": 900000},
            "docs": {"name": "Автогенерация документов", "price": 700000},
        },
    },
    "crm": {
        "name": "CRM-интеграция",
        "base": 9000000,
        "days": 18,
        "options": {
            "migrate": {"name": "Перенос данных", "price": 1200000},
            "tel": {"name": "Телефония и звонки", "price": 1500000},
            "train": {"name": "Обучение команды", "price": 800000},
        },
    },
    "ai": {
        "name": "ИИ-агенты",
        "base": 12000000,
        "days": 21,
        "options": {
            "voice": {"name": "Голосовой бот", "price": 3000000},
            "crm": {"name": "Связь с CRM", "price": 1500000},
            "analytics": {"name": "Аналитика диалогов", "price": 1000000},
        },
    },
}


def day_word(n: int) -> str:
    """Русское склонение «день/дня/дней». Зеркало dayWord() из js/main.js."""
    m10, m100 = n % 10, n % 100
    if m10 == 1 and m100 != 11:
        return "день"
    if 2 <= m10 <= 4 and (m100 < 10 or m100 >= 20):
        return "дня"
    return "дней"


def days_display(days: int, urgent: bool) -> str:
    """Человекочитаемый срок. Зеркало urgentText()/dayWord() из js/main.js.

    days тут — базовая инженерная оценка. При «срочно» показываем сокращённый
    диапазон ровно как на сайте, чтобы админ видел то же обещание, что и клиент.
    """
    if not urgent:
        return f"{days} {day_word(days)}"
    if days <= 2:
        return "12 часов"
    if days <= 4:
        return "1–2 дня"
    lo = math.ceil(days * 0.3)
    hi = math.ceil(days * 0.5)
    return f"{lo}–{hi} {day_word(hi)}"


def calc(service: str, options: list[str], urgent: bool) -> dict:
    """Пересчёт заявки на сервере. Повторяет логику calc() из js/main.js."""
    svc = SERVICES[service]
    price = svc["base"]
    chosen = []
    for oid in options:
        opt = svc["options"][oid]
        price += opt["price"]
        chosen.append(opt["name"])
    days = svc["days"] + math.ceil(len(chosen) * 0.8)
    if urgent:
        price = round(price * 1.3 / 10000) * 10000
    return {
        "service_name": svc["name"],
        "price": price,
        "days": days,
        "days_text": days_display(days, urgent),
        "chosen": chosen,
    }
