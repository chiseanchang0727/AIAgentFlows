import os
import sqlite3


def main():

    db_path = 'local_db.db'

    if not os.path.exists(db_path):
        print("Database does not exist. Creating it...")

    conn = sqlite3.connect(db_path)  # This still creates it if missing

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()
    print("Database ready.")

if __name__ == "__main__":
    main()