import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = "game_chooser_db"
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

def wipe_database():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Disable FK checks temporarily
        cur.execute("SET session_replication_role = 'replica';")

        # Get all table names
        cur.execute("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public';
        """)
        tables = cur.fetchall()

        if not tables:
            print("No tables found in 'public' schema.")
            return

        for (table,) in tables:
            print(f"Clearing table: {table}")
            cur.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")

        # Re-enable FK checks
        cur.execute("SET session_replication_role = 'origin';")

        cur.close()
        conn.close()
        print("✅ Database wiped successfully (schema retained).")

    except Exception as e:
        print(f"❌ Error wiping database: {e}")

if __name__ == "__main__":
    wipe_database()
