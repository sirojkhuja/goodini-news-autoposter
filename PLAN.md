# Goodini News Autoposter Plan

## Objective

Deliver a submission-ready `n8n` automation project for the employer test task:

- Dockerized `n8n` + PostgreSQL stack that starts with one command
- Completed "News Autoposter" workflow
- Mandatory reliability features
- Bonus features: deduplication, RSS/cron ingestion, README
- Workflow notes and repository documentation suitable for review

## Constraints

- Keep secrets out of the repository
- Make the workflow portable for the reviewer
- Prefer environment-variable based integrations over instance-specific stored credentials
- Leave the repo in a state that can be verified locally

## Implementation Strategy

### 1. Repository Scaffolding

- Initialize git repository
- Set remote to `git@github.com:sirojkhuja/goodini-news-autoposter.git`
- Add `.gitignore`
- Add persistent planning documents and keep them updated throughout execution

### 2. Infrastructure

- Fix intentional issues in `docker-compose.yml`
- Improve container persistence and local developer ergonomics
- Expand `env.example` into a complete `.env.example`
- Create local `.env` for validation without committing secrets
- Verify `docker compose config`, build, startup, container health, and exposed services

### 3. Workflow Completion

- Replace placeholder nodes in `Workflow.json`
- Implement:
  - webhook entrypoint
  - input validation
  - duplicate-check branch
  - audio download with `yt-dlp`
  - binary file loading
  - Whisper transcription
  - LLM post generation
  - PostgreSQL persistence
  - Telegram delivery
  - success response
- Make the workflow reviewer-portable by avoiding hardcoded reviewer-local credentials where possible

### 4. Reliability

- Add retry and backoff handling for OpenAI and Telegram
- Add centralized error logging to `error_logs`
- Add Telegram error notification
- Add temp-file cleanup on both success and failure paths

### 5. Bonus Features

- Add URL deduplication with `409` response
- Add schedule-based RSS polling workflow path
- Ensure RSS branch reuses the same processing logic

### 6. Submission Packaging

- Add sticky notes inside the workflow for reviewer guidance
- Write `README.md` with architecture, setup, env vars, runbook, and testing examples
- Perform final validation:
  - lint/format where applicable
  - JSON validity
  - Docker stack validation
  - workflow import sanity
  - repository cleanliness

## Verification Approach

- `docker compose config`
- `docker compose build`
- `docker compose up -d`
- container health and logs
- validate JSON artifacts with `jq`
- validate SQL init file syntax by executing stack startup
- smoke-test webhook locally where possible
- confirm all task list items are completed before final handoff

## Commit Workflow

For each task in `TASKLIST.md`:

1. Mark task as `IN PROGRESS`
2. Implement the task
3. Test, lint, format, and verify
4. Commit with a focused message
5. Push to remote
6. Mark task as `DONE`
