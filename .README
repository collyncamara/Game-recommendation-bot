# Game Recommendation Bot

A small Discord bot + webhook service that recommends a game for your group to play each week based on a shared list of games you already own. Uses PostgreSQL to store the games and state. Designed to run on a Linux server via Docker.

---

## Features
- Store a shared list of games (title, platform, owners, played flag, notes, priority).
- Weekly recommendations posted to a Discord channel (or via webhook).
- Prefer games not yet played; optionally use priority/weighting.
- Simple API/webhook to trigger a recommendation on demand.

---

## Architecture
- Discord bot script (Python/Node/your choice) that reads from Postgres and posts recommendations.
- PostgreSQL (Docker) stores games and play history.
- Optional: small web endpoint to preview/trigger recommendations and manage the list.

---

## Prerequisites
- Linux server with Docker & docker-compose
- Discord bot token and channel ID (or webhook URL)
- Basic familiarity with environment variables

---

## Quick start (recommended)
1. Create a `.env` file with:
    - DISCORD_TOKEN or DISCORD_WEBHOOK_URL
    - DATABASE_URL (or use docker-compose to expose Postgres)
    - SCHEDULE_CRON (optional, e.g. "0 12 * * 1" for Mondays at noon)
    - BOT_OWNER_ID (optional)

2. Example `docker-compose.yml` to run Postgres: