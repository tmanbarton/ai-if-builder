import sqlite3

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS game_data (
            session_id TEXT,
            file_name TEXT,
            content TEXT,
            PRIMARY KEY (session_id, file_name)
        )''')
