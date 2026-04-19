# LevelUp English Bot

Минимальный Telegram-бот для одного пользователя с игровой механикой изучения английского.

## Что уже есть

- `aiogram`-бот с командами `/start`, `/mission`, `/profile`, `/review`, `/boss`, `/help`
- одна стартовая глава `Daily Routine`
- миссии, XP, ранги, ревью ошибок и chapter boss
- простое хранение прогресса в `SQLite`
- готовый `Dockerfile` для деплоя на Railway

## Локальный запуск

1. Создай `.env` по примеру `.env.example`
2. Установи зависимости:

```bash
pip install -r requirements.txt
```

3. Запусти бота:

```bash
python -m bot.main
```

## Переменные окружения

- `TELEGRAM_BOT_TOKEN` — токен бота от BotFather
- `DATABASE_PATH` — путь к sqlite-файлу, по умолчанию `data/levelup.sqlite3`
- `OPENAI_API_KEY` — пока не используется, оставлен под writing-check на следующем этапе
- `GEMINI_API_KEY` — ключ Google Gemini API
- `GEMINI_MODEL` — модель Gemini, по умолчанию `gemini-2.5-flash`

## Деплой на Railway

1. Залей проект на GitHub
2. Создай новый проект в Railway из GitHub-репозитория
3. Railway сам подхватит `Dockerfile`
4. Добавь переменные:
   - `TELEGRAM_BOT_TOKEN`
   - `DATABASE_PATH=data/levelup.sqlite3`
5. Задеплой сервис

Важно: `SQLite` подходит для старта и одного пользователя. Если позже захочешь постоянное хранилище на Railway без риска потери локального файла контейнера, переведем проект на Postgres.
