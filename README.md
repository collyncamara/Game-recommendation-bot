# 🎮 Game Recommendation Bot

A lightweight weekly game-picker for your group: the bot uses a shared list of games you already own, stores selections in PostgreSQL, applies weighting so less-played games are more likely, and posts the result to Discord via webhook.

---

## ✨ Features

- Maintain a list of games with play counts (`times_selected`) in PostgreSQL  
- Weekly (or on-demand) recommendations posted to a Discord channel via webhook  
- Weighted selection — games with fewer selections have higher probability  
- Load games from a `games.csv` file into the database (with initial count `0`)  
- Utility script to wipe all data while preserving the schema  

---

## 🏗️ Architecture

- `docker-compose.yml` runs a PostgreSQL container with persistent storage  
- Python scripts:
  - `game_chooser.py` – main weekly picker script  
  - `wipe_database.py` – utility to truncate all data  
- `.env` holds secrets and config (DB credentials, webhook URL, etc.)  
- Optional `games.csv` file lists games to load initially  

---

## ✅ Prerequisites

- A Linux server (or VM) with Docker & Docker Compose installed  
- PostgreSQL container running from your `docker-compose.yml`  
- Discord webhook URL (create under **Server Settings → Integrations → Webhooks**)  
- `.env` file with required variables (see below)  
- Optional `games.csv` file with a header row `name`  

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/collyncamara/Game-recommendation-bot.git
cd Game-recommendation-bot
