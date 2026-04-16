import sqlite3

import pytest

from backend.database import init_db, insert_file, fetch_file


@pytest.fixture
def test_db(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    return db_path


def test_insert_and_fetch_roundtrip(test_db):
    insert_file("session-1", "foo.txt", "hello world", test_db)

    result = fetch_file("session-1", "foo.txt", test_db)

    assert result == "hello world"


def test_insert_duplicate_key_raises(test_db):
    insert_file("session-1", "foo.txt", "first", test_db)

    with pytest.raises(sqlite3.IntegrityError):
        insert_file("session-1", "foo.txt", "second", test_db)


def test_fetch_missing_returns_none(test_db):
    result = fetch_file("nonexistent-session", "nonexistent.txt", test_db)

    assert result is None
