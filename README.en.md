# Goodini News Autoposter

Language: [Русский](README.md) | [English](README.en.md)

Test-task implementation for an `n8n Automation Engineer` assignment.

The project delivers:

- Dockerized `n8n` + PostgreSQL stack
- Webhook-based news autoposter workflow
- Audio download with `yt-dlp`
- Whisper transcription
- LLM-based Telegram post generation
- PostgreSQL persistence
- Telegram delivery
- Error logging, alerts, retries, and temp-file cleanup
- Bonus features: deduplication and RSS/schedule ingestion

## Repository Layout

- `docker-compose.yml`: local stack definition
- `Dockerfile.n8n`: custom `n8n` image with `yt-dlp`, `ffmpeg`, Python, and PostgreSQL client
- `.env.example`: environment variable template
- `init.sql`: creates `news_posts` and `error_logs`
- `Workflow.json`: importable workflow definition
- `tools/generate_workflow.py`: source-of-truth generator for `Workflow.json`
- `scripts/download_audio.sh`: safe wrapper around `yt-dlp`
- `scripts/db_ops.py`: database helper used by workflow shell steps

## What Was Fixed

Infrastructure fixes:

- fixed broken `n8n -> PostgreSQL` host wiring in Compose
- added persistent `n8n` storage
- replaced the old env template with a complete `.env.example`
- pinned `n8n` to `1.82.3` because the current `latest` image is hardened and no longer allows package installation
- corrected the `n8n` healthcheck to use `127.0.0.1`

Workflow fixes:

- replaced all placeholder `No Op` nodes
- fixed webhook validation and proper `400` response
- implemented retries and explicit error branches
- removed dependence on reviewer-local n8n credentials by using env vars and helper scripts

## Workflow Design

Main webhook path:

1. `POST /webhook/news-autoposter`
2. Validate input `{ "url": "...", "id": "..." }`
3. Deduplicate by `source_url`
4. Download audio with `yt-dlp`
5. Read binary file
6. Transcribe with Whisper (`ru`)
7. Generate Telegram post with OpenAI
8. Save draft row in PostgreSQL
9. Send to Telegram
10. Update row status to `published`
11. Cleanup temp file
12. Respond to webhook

Reliability path:

- Whisper retries: `5s`, `15s`, `30s`
- OpenAI generation retries: `5s`, `15s`, `30s`
- Telegram delivery retry: `5s`
- all normalized failures:
  - write to `error_logs`
  - send Telegram error alert
  - cleanup temp file
  - return structured webhook error response

Bonus path:

- `Schedule Trigger` + `RSS Read`
- RSS items are normalized into the same shared pipeline as webhook requests
- duplicate RSS items are skipped without webhook response

## Environment Variables

Required:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `N8N_ENCRYPTION_KEY`
- `OPENAI_API_KEY`
- `OPENAI_CHAT_MODEL`
- `OPENAI_TRANSCRIPTION_MODEL`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Useful local defaults:

- `WEBHOOK_URL=http://localhost:5678/`
- `N8N_EDITOR_BASE_URL=http://localhost:5678`
- `GENERIC_TIMEZONE=Asia/Tashkent`
- `RSS_FEED_URL=<your RSS feed>`

## Local Setup

1. Create `.env` from `.env.example`.
2. Fill real OpenAI and Telegram credentials.
3. Start the stack:

```bash
docker compose up -d --build
```

4. Open `http://localhost:5678`.
5. Import `Workflow.json` in the n8n UI.
6. Activate the workflow.

## Local Verification

Validated locally:

- `docker compose config`
- `docker compose up -d --build`
- `n8n` health: `http://localhost:5678/healthz`
- workflow import into running `n8n`
- webhook validation path
- duplicate detection path
- download failure path
- error logging into PostgreSQL
- temp-file cleanup in `/tmp/news-autoposter`
- live happy-path execution with real OpenAI and Telegram credentials

Smoke-test examples:

Missing URL:

```bash
curl -i -X POST http://localhost:5678/webhook/news-autoposter \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Expected: `400 Bad Request`

Duplicate URL:

```bash
curl -i -X POST http://localhost:5678/webhook/news-autoposter \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","id":"dup-1"}'
```

Expected: `409 Conflict`

Invalid/non-downloadable URL:

```bash
curl -i -X POST http://localhost:5678/webhook/news-autoposter \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://nonexistent-123.invalid/video","id":"bad-url"}'
```

Expected: `422 Unprocessable Entity` and a row in `error_logs`

Real end-to-end example:

```bash
curl -i -X POST http://localhost:5678/webhook/news-autoposter \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://www.youtube.com/watch?v=dGLtsqaExSo","id":"demo-live-run"}'
```

Expected: `201 Created`, a `published` row in `news_posts`, and a Telegram message

## Important Note About Live Integrations

The full happy-path execution requires real credentials:

- OpenAI for Whisper + LLM generation
- Telegram Bot API for message delivery and error alerts

The repository is fully wired for those integrations, but live end-to-end success cannot be verified without valid secrets.

## Workflow Generation

`Workflow.json` is generated from:

```bash
python3 tools/generate_workflow.py
```

This makes the workflow easier to maintain than editing large escaped JSON by hand.
