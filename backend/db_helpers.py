from backend.database import insert_file, does_file_exist, update_file, fetch_file_content


def insert(session_id: str, file_name: str, code: str):
    insert_file(session_id, file_name, code)


def upsert(session_id: str, file_name: str, code: str):
    if does_file_exist(session_id, file_name):
        update_file(session_id, file_name, code)
    else:
        insert_file(session_id, file_name, code)


def append(session_id: str, file_name: str, code: str):
    if does_file_exist(session_id, file_name):
        contents: str = fetch_file_content(session_id, file_name)
        contents += "\n\n" + code
        update_file(session_id, file_name, contents)
    else:
        insert_file(session_id, file_name, code)