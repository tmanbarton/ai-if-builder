import pytest

from backend.build_map import write_files
from backend.database import init_db, fetch_file
from backend.models.connection import Connection
from backend.models.item import Item
from backend.models.location import Location

TEST_LOCATION = Location(
    name="dark cave",
    short_description="dark cave short description",
    long_description="dark cave long description",
)
TEST_ITEM = Item(name="key",
                 inventory_description="key inventory description",
                 location_description="key location description",
                 detailed_description="key detailed description",
                 aliases=["key ring"],
                 location="dark cave")

@pytest.fixture
def test_db(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    return db_path

def test_single_location_constants(test_db):

    session_id: str = write_files([TEST_LOCATION], [], [], test_db)

    content: str = fetch_file(session_id, "Constants.java", test_db)[0]
    assert 'public static final String DARK_CAVE_NAME = "dark cave";' in content
    assert 'public static final String DARK_CAVE_SHORT_DESCRIPTION = "dark cave short description";' in content
    assert 'public static final String DARK_CAVE_LONG_DESCRIPTION = "dark cave long description";' in content

def test_single_item_constants(test_db):
    session_id: str = write_files([], [], [TEST_ITEM], test_db)

    content: str = fetch_file(session_id, "Constants.java", test_db)[0]
    assert 'public static final String KEY_NAME = "key";' in content
    assert 'public static final String KEY_INVENTORY_DESCRIPTION = "key inventory description";' in content
    assert 'public static final String KEY_LOCATION_DESCRIPTION = "key location description";' in content
    assert 'public static final String KEY_DETAILED_DESCRIPTION = "key detailed description";' in content
    assert 'public static final Set<String> KEY_ALIASES = Set.of("key ring");' in content

def test_multiple_aliases_item_constants(test_db):
    item = Item(name="rope",
                inventory_description="rope inventory description",
                location_description="rope location description",
                detailed_description="rope detailed description",
                aliases=["rope", "cord", "string"],
                location="barn")
    session_id: str = write_files([], [], [item], test_db)

    content: str = fetch_file(session_id, "Constants.java", test_db)[0]
    assert 'public static final Set<String> ROPE_ALIASES = Set.of("rope", "cord", "string");' in content

def test_add_location(test_db):
    session_id: str = write_files([TEST_LOCATION], [], [], test_db)
    content: str = fetch_file(session_id, "map.txt", test_db)[0]
    expected = """
.addLocation(new Location(
  Constants.DARK_CAVE_NAME,
  Constants.DARK_CAVE_LONG_DESCRIPTION,
  Constants.DARK_CAVE_SHORT_DESCRIPTION))"""

    assert expected in content

def test_add_item(test_db):
    session_id: str = write_files([], [], [TEST_ITEM], test_db)
    content: str = fetch_file(session_id, "map.txt", test_db)[0]
    expected = """
.placeItem(new Item(
  Constants.KEY_NAME,
  Constants.KEY_INVENTORY_DESCRIPTION,
  Constants.KEY_LOCATION_DESCRIPTION,
  Constants.KEY_DETAILED_DESCRIPTION,
  Constants.KEY_ALIASES),
  Constants.DARK_CAVE_NAME))"""

    assert expected in content

def test_connect_locations(test_db):
    target_location = Location(
        name="hall of the mountain king",
        short_description="hall of the mountain king short description",
        long_description="hall of the mountain king long description",
    )
    connection = Connection(
        source_location=TEST_LOCATION.name,
        target_location=target_location.name,
        direction="NORTH")
    session_id: str = write_files([TEST_LOCATION, target_location],[connection], [], test_db)
    content: str = fetch_file(session_id, "map.txt", test_db)[0]

    expected = ".connectOneWay(Constants.DARK_CAVE_NAME, Direction.NORTH, Constants.HALL_OF_THE_MOUNTAIN_KING_NAME)"
    assert expected in content


def test_empty_aliases(test_db):
    item = Item(name="torch",
                inventory_description="torch inventory description",
                location_description="torch location description",
                detailed_description="torch detailed description",
                aliases=[],
                location="dark cave")
    session_id: str = write_files([], [], [item], test_db)

    content: str = fetch_file(session_id, "Constants.java", test_db)[0]
    assert 'TORCH_ALIASES = Set.of();' in content


def test_starting_location_sets_starting(test_db):
    location = Location(
        name="entrance hall",
        short_description="entrance hall short description",
        long_description="entrance hall long description",
        is_starting_location=True,
    )
    session_id: str = write_files([location], [], [], test_db)

    content: str = fetch_file(session_id, "map.txt", test_db)[0]
    assert ".setStartingLocation(Constants.ENTRANCE_HALL_NAME)" in content


def test_non_starting_location_no_starting_set(test_db):
    session_id: str = write_files([TEST_LOCATION], [], [], test_db)

    content: str = fetch_file(session_id, "map.txt", test_db)[0]
    assert ".setStartingLocation" not in content


def test_multi_word_name_screaming_snake_case(test_db):
    item = Item(name="rusty old key",
                inventory_description="rusty old key inventory description",
                location_description="rusty old key location description",
                detailed_description="rusty old key detailed description",
                aliases=[],
                location="dark cave")
    session_id: str = write_files([], [], [item], test_db)

    content: str = fetch_file(session_id, "Constants.java", test_db)[0]
    assert 'RUSTY_OLD_KEY_NAME = "rusty old key";' in content


def test_full_map(test_db):
    entrance = Location(
        name="entrance",
        short_description="entrance short description",
        long_description="entrance long description",
        is_starting_location=True,
    )
    cellar = Location(
        name="wine cellar",
        short_description="wine cellar short description",
        long_description="wine cellar long description",
    )
    lantern = Item(name="lantern",
                   inventory_description="lantern inventory description",
                   location_description="lantern location description",
                   detailed_description="lantern detailed description",
                   aliases=["lamp", "light"],
                   location="entrance")
    connection = Connection(
        source_location="entrance",
        target_location="wine cellar",
        direction="DOWN",
    )

    session_id: str = write_files([entrance, cellar], [connection], [lantern], test_db)

    # Verify Constants.java
    constants = fetch_file(session_id, "Constants.java", test_db)[0]

    # Section headers
    assert "///// Item constants /////" in constants
    assert "///// Location constants /////" in constants

    # Lantern item constants
    assert 'LANTERN_NAME = "lantern";' in constants
    assert 'LANTERN_INVENTORY_DESCRIPTION = "lantern inventory description";' in constants
    assert 'LANTERN_LOCATION_DESCRIPTION = "lantern location description";' in constants
    assert 'LANTERN_DETAILED_DESCRIPTION = "lantern detailed description";' in constants
    assert 'LANTERN_ALIASES = Set.of("lamp", "light");' in constants

    # Entrance location constants
    assert 'ENTRANCE_NAME = "entrance";' in constants
    assert 'ENTRANCE_SHORT_DESCRIPTION = "entrance short description";' in constants
    assert 'ENTRANCE_LONG_DESCRIPTION = "entrance long description";' in constants

    # Wine cellar location constants
    assert 'WINE_CELLAR_NAME = "wine cellar";' in constants
    assert 'WINE_CELLAR_SHORT_DESCRIPTION = "wine cellar short description";' in constants
    assert 'WINE_CELLAR_LONG_DESCRIPTION = "wine cellar long description";' in constants

    # Verify map.txt
    map_txt = fetch_file(session_id, "map.txt", test_db)[0]

    # Section headers
    assert "///// Add Items /////" in map_txt
    assert "///// Add Locations /////" in map_txt
    assert "///// Connect Locations /////" in map_txt

    # Lantern placement
    assert """.placeItem(new Item(
  Constants.LANTERN_NAME,
  Constants.LANTERN_INVENTORY_DESCRIPTION,
  Constants.LANTERN_LOCATION_DESCRIPTION,
  Constants.LANTERN_DETAILED_DESCRIPTION,
  Constants.LANTERN_ALIASES),
  Constants.ENTRANCE_NAME))""" in map_txt

    # Entrance location added with starting location
    assert """.addLocation(new Location(
  Constants.ENTRANCE_NAME,
  Constants.ENTRANCE_LONG_DESCRIPTION,
  Constants.ENTRANCE_SHORT_DESCRIPTION))""" in map_txt
    assert ".setStartingLocation(Constants.ENTRANCE_NAME)" in map_txt

    # Wine cellar location added without starting location
    assert """.addLocation(new Location(
  Constants.WINE_CELLAR_NAME,
  Constants.WINE_CELLAR_LONG_DESCRIPTION,
  Constants.WINE_CELLAR_SHORT_DESCRIPTION))""" in map_txt
    assert map_txt.count(".setStartingLocation") == 1

    # Connection
    assert ".connectOneWay(Constants.ENTRANCE_NAME, Direction.DOWN, Constants.WINE_CELLAR_NAME)" in map_txt
