import pytest

from backend.create_intro import write_files
from backend.database import init_db, fetch_file
from backend.models.custom_intro_response import CustomIntroResponse

EMPTY_INTRO_RESPONSE = CustomIntroResponse(yes_answer="", no_answer="")


@pytest.fixture
def test_db(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    return db_path


def test_skip_intro_writes_skip_intro_call(test_db):
    session_id = write_files(
        should_skip_intro=True,
        game_intro=None,
        intro_response=EMPTY_INTRO_RESPONSE,
        intro_answer=[],
        db_name=test_db,
    )

    content = fetch_file(session_id, "intro-info.txt", test_db)

    assert content == ".skipIntro()"


def test_game_intro_writes_game_intro_call(test_db):
    session_id = write_files(
        should_skip_intro=False,
        game_intro="welcome to the cave",
        intro_response=EMPTY_INTRO_RESPONSE,
        intro_answer=[],
        db_name=test_db,
    )

    content = fetch_file(session_id, "intro-info.txt", test_db)

    assert content == '.gameIntro("welcome to the cave")'


def test_intro_response_writes_with_intro_response_call(test_db):
    intro_response = CustomIntroResponse(
        yes_answer="you chose yes",
        no_answer="you chose no",
    )

    session_id = write_files(
        should_skip_intro=False,
        game_intro=None,
        intro_response=intro_response,
        intro_answer=[],
        db_name=test_db,
    )

    content = fetch_file(session_id, "intro-info.txt", test_db)

    assert content == '.withIntroResponse("you chose yes", "you chose no")'


def test_no_intro_info_writes_empty_content(test_db):
    session_id = write_files(
        should_skip_intro=False,
        game_intro=None,
        intro_response=EMPTY_INTRO_RESPONSE,
        intro_answer=[],
        db_name=test_db,
    )

    content = fetch_file(session_id, "intro-info.txt", test_db)

    assert content == ""


def test_skip_intro_and_game_intro_combined(test_db):
    session_id = write_files(
        should_skip_intro=True,
        game_intro="welcome to the cave",
        intro_response=EMPTY_INTRO_RESPONSE,
        intro_answer=[],
        db_name=test_db,
    )

    content = fetch_file(session_id, "intro-info.txt", test_db)

    assert content == '.skipIntro().gameIntro("welcome to the cave")'