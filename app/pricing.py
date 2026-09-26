"""Зеркало SERVICES из фронтенда (js/main.js).

Цена и срок ВСЕГДА считаются здесь, на бэкенде. Числу, пришедшему
с сайта, не доверяем — иначе клиент подделает сумму заявки.
Держи в синхроне с js/main.js при изменении цен/опций.
"""
import math

SERVICES = {
    "landing": {
        "name": "Лендинг",
        "base": 950000,
        "days": 5,
        "options": {
            "anim": {"name": "Анимации и микро-взаимодействия", "price": 120000},
            "lang2": {"name": "Вторая языковая версия (UZ или RU)", "price": 150000},
            "pay": {"name": "Приём оплаты Click / Payme", "price": 200000},
            "seo": {"name": "SEO-база и подключение аналитики", "price": 100000},
            "host": {"name": "Хостинг и домен (любая зона) на год", "price": 250000},
        },
    },
    "site": {
        "name": "Сайт компании",
        "base": 3800000,
        "days": 10,
        "options": {
            "admin": {"name": "Админ-панель — сами меняете контент", "price": 1260000},
            "blog": {"name": "Раздел новостей или блога", "price": 420000},
            "lang2": {"name": "Вторая языковая версия (UZ или RU)", "price": 500000},
            "tg": {"name": "Заявки с сайта в Telegram", "price": 340000},
            "crm": {"name": "Интеграция с CRM", "price": 2100000},
            "host": {"name": "Хостинг и домен (любая зона) на год", "price": 590000},
        },
    },
    "bot": {
        "name": "Telegram-бот",
        "base": 1000000,
        "days": 7,
        "options": {
            "pay": {"name": "Приём платежей в боте", "price": 300000},
            "admin": {"name": "Админ-панель для управления ботом", "price": 300000},
            "mail": {"name": "Рассылки по базе клиентов", "price": 150000},
            "site": {"name": "Интеграция с вашим сайтом", "price": 200000},
        },
    },
    "wedding": {
        "name": "Свадебное приглашение",
        "base": 120000,
        "days": 3,
        "options": {
            "guests": {"name": "Личные ссылки для каждого гостя", "price": 30000},
            "rsvp": {"name": "Ответы гостей вам в Telegram", "price": 0},
            "music": {"name": "Музыка и анимация открытия", "price": 0},
            "map": {"name": "Карта и маршрут до зала", "price": 0},
        },
    },
    "shop": {
        "name": "Интернет-магазин",
        "base": 5900000,
        "days": 14,
        "options": {
            "pay": {"name": "Оплата Click / Payme", "price": 700000},
            "stock": {"name": "Учёт склада и остатков", "price": 840000},
            "bot": {"name": "Telegram-бот магазина", "price": 1010000},
            "delivery": {"name": "Доставка и статусы заказов", "price": 500000},
            "crm": {"name": "Интеграция с CRM и складом", "price": 2100000},
            "host": {"name": "Хостинг и домен (любая зона) на год", "price": 590000},
        },
    },
    "optim": {
        "name": "Оптимизация бизнес-процессов",
        "base": 5000000,
        "days": 14,
        "options": {
            "audit": {"name": "Глубокий аудит отделов", "price": 0},
            "docs": {"name": "Регламенты и инструкции", "price": 670000},
            "auto": {"name": "Автоматизация одного процесса", "price": 1010000},
        },
    },
    "hr": {
        "name": "HR-интеграция",
        "base": 5900000,
        "days": 16,
        "options": {
            "ats": {"name": "Трекер кандидатов (ATS)", "price": 1260000},
            "bot": {"name": "HR-бот в Telegram", "price": 760000},
            "docs": {"name": "Автогенерация документов", "price": 590000},
        },
    },
    "crm": {
        "name": "CRM-интеграция",
        "base": 7600000,
        "days": 18,
        "options": {
            "migrate": {"name": "Перенос данных", "price": 1010000},
            "tel": {"name": "Телефония и звонки", "price": 1260000},
            "train": {"name": "Обучение команды", "price": 670000},
        },
    },
    "ai": {
        "name": "ИИ-агенты",
        "base": 10100000,
        "days": 21,
        "options": {
            "voice": {"name": "Голосовой бот", "price": 2520000},
            "crm": {"name": "Связь с CRM", "price": 1260000},
            "analytics": {"name": "Аналитика диалогов", "price": 840000},
        },
    },
    "odoo": {
        "name": "Внедрение ODOO",
        "base": 9800000,
        "days": 20,
        "options": {
            "migrate": {"name": "Перенос текущих данных", "price": 1400000},
            "modules": {"name": "Настройка модулей (склад, бухгалтерия, CRM)", "price": 1750000},
            "integrate": {"name": "Интеграция с сайтом и ботом", "price": 1050000},
            "train": {"name": "Обучение команды", "price": 700000},
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
