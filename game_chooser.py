# Install dependencies:
# sudo apt install python3 python3-pip
# pip3 install psycopg2-binary requests python-dotenv

#!/usr/bin/env python3
import os
import csv
import random
import requests
import psycopg2
from dotenv import load_dotenv

# ==== LOAD ENVIRONMENT ====
load_dotenv()  # Loads variables from .env file

DB_CONFIG = {
    "dbname": "game_chooser_db",
    "user": os.getenv("POSTGRES_USER", "gamebot"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": 5432,
}

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")
ALPHA = float(os.getenv("ALPHA", 1.5))
# ===========================
def load_games_from_csv(conn, csv_path="games.csv"):
    """
    Reads a CSV file containing game names and inserts them into the database
    if they don't already exist. Initializes times_selected to 0.
    """
    added = 0
    skipped = 0

    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        if "name" not in reader.fieldnames:
            print("CSV missing required 'name' column header.")
            return

        with conn.cursor() as cur:
            for row in reader:
                name = row["name"].strip()
                if not name:
                    continue
                try:
                    cur.execute(
                        "INSERT INTO games (name, times_selected) VALUES (%s, 0) ON CONFLICT (name) DO NOTHING;",
                        (name,)
                    )
                    # cur.rowcount is unreliable for ON CONFLICT, so check manually
                    cur.execute("SELECT 1 FROM games WHERE name = %s;", (name,))
                    if cur.fetchone():
                        added += 1
                except Exception as e:
                    print(f"Error inserting {name}: {e}")
                    skipped += 1

        conn.commit()

    print(f"Games loaded from CSV: {added} added, {skipped} skipped")

def get_games(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT name, times_selected FROM games;")
        return cur.fetchall()

def choose_weighted(games):
    weights = [1 / ((count + 1) ** ALPHA) for _, count in games]
    total = sum(weights)
    normalized = [w / total for w in weights]
    chosen = random.choices(games, weights=normalized, k=1)[0]
    return chosen[0]

def increment_game(conn, game_name):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE games SET times_selected = times_selected + 1 WHERE name = %s;",
            (game_name,)
        )
    conn.commit()

import requests

def get_game_thumbnail(game_name):
    """
    Try to find a thumbnail for the game using Steam's public search API.
    Returns a URL or None if not found.
    """
    try:
        resp = requests.get(
            "https://store.steampowered.com/api/storesearch/",
            params={"term": game_name, "cc": "us"},
            timeout=5
        )
        data = resp.json()
        if "items" in data and len(data["items"]) > 0:
            # Example field: data["items"][0]["tiny_image"]
            return data["items"][0].get("tiny_image")
    except Exception as e:
        print(f"Thumbnail lookup failed: {e}")
    return None

def post_to_discord(game_name):
    if not DISCORD_WEBHOOK:
        print("No Discord webhook set — skipping post.")
        return

    thumbnail_url = get_game_thumbnail(game_name)
    embed = {
        "username": "🎮 Game Picker Bot",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2331/2331852.png", 
        "title": "🎮 Weekly Game Pick!",
        "description": f"This week’s game is **{game_name}**!",
        "color": 0x7289DA,  # Discord blurple
    }

    if thumbnail_url:
        embed["image"] = {"url": thumbnail_url}
        print("Thumbnail found for game:", thumbnail_url)

    payload = {"embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Posted to Discord: {game_name}")
    except Exception as e:
        print(f"Failed to post to Discord: {e}")


def main():
    conn = psycopg2.connect(**DB_CONFIG)

    # Load any new games from CSV first
    load_games_from_csv(conn, "games.csv")

    games = get_games(conn)

    if not games:
        print("No games found in database.")
        return

    chosen_game = choose_weighted(games)
    increment_game(conn, chosen_game)

    print(f"This week's pick: {chosen_game}")
    post_to_discord(chosen_game)

    conn.close()

if __name__ == "__main__":
    main()
