import sqlite3

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS game_data (
            session_id TEXT,
            file_name TEXT,
            content TEXT,
            PRIMARY KEY (session_id, file_name)
        )''')
    conn.close()

def insert_file(session_id: str, file_name: str, content: str):
    """
    Insert file into SQLite database. todo
    :param session_id:
    :param file_name:
    :param content:
    """
    with sqlite3.connect('database.db') as conn:
        conn.execute('INSERT INTO game_data (session_id, file_name, content) VALUES (?, ?, ?)', (session_id, file_name, content))
    conn.close()

# def fetch_file(session_id: str, file_name: str):
