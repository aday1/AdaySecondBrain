import sqlite3
import json

def check_database():
    conn = sqlite3.connect('db/pkm.db')
    cursor = conn.cursor()

    tables = ['daily_metrics', 'daily_entries', 'sub_daily_moods', 'work_logs', 'habit_logs', 'alcohol_logs']

    for table in tables:
        print(f"\nChecking {table}:")
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"Total rows: {count}")

        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        rows = cursor.fetchall()
        for row in rows:
            print(json.dumps(row, default=str, indent=2))

    conn.close()

if __name__ == "__main__":
    check_database()
