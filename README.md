# OREE Telegram Bot 🤖

Інформаційний Telegram-бот для моніторингу цін з сайту ОРЕЕ з алгоритмом розрахунків та Firebase базою даних.

## ✨ Функціональність

- 📊 Автоматичний моніторинг цін ОРЕЕ кожні 5 хвилин
- 🔄 Обробка та розрахунок даних за заданою формулою
- 💾 Збереження даних в Firebase Firestore
- 📱 Telegram-бот з командами для отримання інформації
- 📈 Історія розрахунків та цін
- 📋 Журнал подій моніторингу

## 🛠️ Технологічний стек

- **Python 3.12** — основна мова
- **aiogram 3** — Telegram Bot API
- **Firebase Admin SDK** — база даних Firestore
- **APScheduler** — планувальник задач
- **httpx** — асинхронний HTTP-клієнт
- **BeautifulSoup4** — парсинг HTML
- **Docker** — контейнеризація

## 📋 Структура проєкту

```text
oree-telegram-bot/
├── app/
│   ├── bot/              # Telegram-бот
│   ├── scraper/          # Парсинг сайту ОРЕЕ
│   ├── calculator/       # Розрахунки
│   ├── database/         # Firebase інтеграція
│   ├── config.py         # Конфігурація
│   └── main.py           # Точка входу
├── .env.example          # Приклад змінних оточення
├── requirements.txt      # Python-залежності
├── Dockerfile            # Docker-конфігурація
└── README.md             # Документація
```

## 🚀 Запуск

### 1. Клонування репозиторію

```bash
git clone https://github.com/KostiaBondarchuk1/oree-telegram-bot.git
cd oree-telegram-bot
```

### 2. Налаштування оточення

```bash
cp .env.example .env
```

Заповніть `.env` реальним токеном Telegram і Firebase credentials. Не додавайте `.env` або service-account ключі до Git.

### 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 4. Запуск бота

```bash
python -m app.main
```

### 5. Запуск з Docker

```bash
docker build -t oree-bot .
docker run --env-file .env oree-bot
```

## 📝 Структура Firebase Firestore

```text
/prices/{date}
  - data: {...}
  - timestamp: Timestamp
  - date: string

/calculations/{date}
  - data: {...}
  - timestamp: Timestamp
  - date: string

/users/{telegram_user_id}
  - user_id: int
  - joined_at: Timestamp
  - ...

/monitoring_logs/{log_id}
  - type: string
  - message: string
  - data: {...}
  - timestamp: Timestamp
```

## 🤖 Команди Telegram

- `/start` — запуск бота
- `/prices` — останні ціни
- `/calculate` — виконати розрахунки
- `/status` — статус моніторингу
- `/help` — допомога

## 🔐 Налаштування Firebase

1. Відкрийте [Firebase Console](https://console.firebase.google.com/).
2. Створіть або виберіть проєкт.
3. Увімкніть Cloud Firestore.
4. У **Project Settings → Service Accounts** створіть service-account key.
5. Передайте значення через змінні `.env` або секрети хостингу.

## 🌐 Безкоштовний хостинг

Для постійного процесу моніторингу найкраще підходить Oracle Cloud Always Free. Google Cloud Run може працювати в межах безкоштовної квоти, але потребує окремого налаштування. Render Free може засинати, тому для перевірки кожні 5 хвилин він менш надійний.

## 📊 Формула розрахунку

Фінальна формула буде додана після отримання прикладу Excel-таблиці та опису полів.

## ⚠️ Поточний статус

Проєкт має початковий каркас. Реальний парсинг таблиці ОРЕЕ, дедуплікація, фінальний розрахунок і автоматична розсилка ще потребують реалізації та тестування.
