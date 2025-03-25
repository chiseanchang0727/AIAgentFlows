import os
import sqlite3


def main():
    db_path = 'local_db.db'

    if not os.path.exists(db_path):
        print("Database does not exist. Creating it...")

    conn = sqlite3.connect(db_path)  # This still creates it if missing
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    # Sample data to insert
    sample_users = [("Alice",), ("Bob",), ("Charlie",)]

    # Insert sample data (only if table is empty)
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executemany("INSERT INTO users (name) VALUES (?)", sample_users)
        print(f"Inserted {len(sample_users)} sample users.")
    else:
        print("Users already exist. Skipping insert.")

    conn.commit()
    conn.close()
    print("Database ready.")

if __name__ == "__main__":
    main()
