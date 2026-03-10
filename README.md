# Goodini News Autoposter

Language: [Русский](README.md) | [English](README.en.md)

Реализация тестового задания на позицию `n8n Automation Engineer`.

Проект включает:

- Docker-стек с `n8n` и PostgreSQL
- workflow автопостинга новостей через webhook
- загрузку аудио через `yt-dlp`
- транскрибацию через Whisper
- генерацию Telegram-поста через LLM
- сохранение данных в PostgreSQL
- отправку сообщений в Telegram
- логирование ошибок, алерты, ретраи и очистку временных файлов
- бонусные функции: дедупликация и ingestion через RSS/расписание

## Структура Репозитория

- `docker-compose.yml`: локальный стек
- `Dockerfile.n8n`: кастомный образ `n8n` с `yt-dlp`, `ffmpeg`, Python и PostgreSQL client
- `.env.example`: шаблон переменных окружения
- `init.sql`: создание таблиц `news_posts` и `error_logs`
- `Workflow.json`: импортируемое описание workflow
- `tools/generate_workflow.py`: исходный генератор для `Workflow.json`
- `scripts/download_audio.sh`: безопасная обертка над `yt-dlp`
- `scripts/db_ops.py`: helper-скрипт для операций с БД из workflow

## Что Было Исправлено

Инфраструктура:

- исправлена сломанная связка `n8n -> PostgreSQL` в Compose
- добавлено постоянное хранилище для `n8n`
- старый шаблон env заменен на полный `.env.example`
- `n8n` зафиксирован на версии `1.82.3`, потому что актуальный `latest`-образ уже не позволяет ставить пакеты так, как требуется в задании
- исправлен healthcheck `n8n`, теперь он использует `127.0.0.1`

Workflow:

- заменены все placeholder-узлы `No Op`
- исправлена валидация webhook и корректный ответ `400`
- добавлены ретраи и явные error-ветки
- убрана зависимость от локальных reviewer credentials в `n8n`: интеграции работают через env vars и helper-скрипты

## Архитектура Workflow

Основной webhook-сценарий:

1. `POST /webhook/news-autoposter`
2. Валидация входных данных `{ "url": "...", "id": "..." }`
3. Дедупликация по `source_url`
4. Загрузка аудио через `yt-dlp`
5. Чтение бинарного файла
6. Транскрибация через Whisper (`ru`)
7. Генерация Telegram-поста через OpenAI
8. Сохранение draft-записи в PostgreSQL
9. Отправка в Telegram
10. Обновление статуса записи на `published`
11. Очистка временного файла
12. Ответ webhook-запросу

Путь надежности:

- ретраи Whisper: `5s`, `15s`, `30s`
- ретраи генерации OpenAI: `5s`, `15s`, `30s`
- ретрай отправки в Telegram: `5s`
- каждая нормализованная ошибка:
  - записывается в `error_logs`
  - отправляет Telegram-алерт
  - запускает очистку временного файла
  - возвращает структурированный webhook-ответ с ошибкой

Бонусный путь:

- `Schedule Trigger` + `RSS Read`
- RSS-элементы нормализуются в тот же pipeline, что и webhook
- дубликаты из RSS тихо пропускаются без webhook-ответа

## Переменные Окружения

Обязательные:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `N8N_ENCRYPTION_KEY`
- `OPENAI_API_KEY`
- `OPENAI_CHAT_MODEL`
- `OPENAI_TRANSCRIPTION_MODEL`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Полезные локальные значения по умолчанию:

- `WEBHOOK_URL=http://localhost:5678/`
- `N8N_EDITOR_BASE_URL=http://localhost:5678`
- `GENERIC_TIMEZONE=Asia/Tashkent`
- `RSS_FEED_URL=<ваш RSS feed>`

## Локальный Запуск

1. Создать `.env` из `.env.example`.
2. Заполнить реальные OpenAI и Telegram credentials.
3. Поднять стек:

```bash
docker compose up -d --build
```

4. Открыть `http://localhost:5678`.
5. Импортировать `Workflow.json` в UI `n8n`.
6. Активировать workflow.

## Локальная Проверка

Локально уже проверено:

- `docker compose config`
- `docker compose up -d --build`
- healthcheck `n8n`: `http://localhost:5678/healthz`
- импорт workflow в работающий `n8n`
- ветка валидации webhook
- ветка дедупликации
- ветка ошибки загрузки
- логирование ошибок в PostgreSQL
- очистка временных файлов в `/tmp/news-autoposter`
- реальный happy-path с рабочими OpenAI и Telegram credentials

Примеры smoke-тестов:

Отсутствует URL:

```bash
curl -i -X POST http://localhost:5678/webhook/news-autoposter \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Ожидается: `400 Bad Request`

Дубликат URL:

```bash
curl -i -X POST http://localhost:5678/webhook/news-autoposter \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","id":"dup-1"}'
```

Ожидается: `409 Conflict`

Невалидный или недоступный URL:

```bash
curl -i -X POST http://localhost:5678/webhook/news-autoposter \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://nonexistent-123.invalid/video","id":"bad-url"}'
```

Ожидается: `422 Unprocessable Entity` и запись в `error_logs`

Реальный end-to-end пример:

```bash
curl -i -X POST http://localhost:5678/webhook/news-autoposter \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://www.youtube.com/watch?v=dGLtsqaExSo","id":"demo-live-run"}'
```

Ожидается: `201 Created`, запись со статусом `published` в `news_posts` и сообщение в Telegram

## Важное Замечание По Live-Интеграциям

Для полного happy-path нужны реальные credentials:

- OpenAI для Whisper и генерации поста
- Telegram Bot API для отправки сообщений и error-alerts

Репозиторий полностью подготовлен для этих интеграций, но полноценный live-success нельзя проверить без реальных секретов.

## Генерация Workflow

`Workflow.json` генерируется командой:

```bash
python3 tools/generate_workflow.py
```

Так workflow поддерживать проще, чем редактировать большой JSON с экранированными строками вручную.
