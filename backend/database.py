import sqlite3

def init_db(db_name: str = 'database.db'):
    with sqlite3.connect(db_name) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS game_data (
            session_id TEXT,
            file_name TEXT,
            content TEXT,
            PRIMARY KEY (session_id, file_name)
        )''')

def insert_file(session_id: str, file_name: str, content: str, db_name: str = 'database.db'):
    with sqlite3.connect(db_name) as conn:
        conn.execute('INSERT INTO game_data (session_id, file_name, content) VALUES (?, ?, ?)', (session_id, file_name, content))

def fetch_file(session_id: str, file_name: str, db_name: str = 'database.db'):
    with sqlite3.connect(db_name) as conn:
        cursor: sqlite3.Cursor = conn.execute('SELECT content FROM game_data WHERE session_id = ? AND file_name = ?', (session_id, file_name))
        row = cursor.fetchone()
    return row[0] if row is not None else None

def clear_data(db_name: str = 'database.db'):
    with sqlite3.connect(db_name) as conn:
        conn.execute('DELETE FROM game_data')
