from backend.build_map import write_files
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

def test_single_location_constants(tmp_path):

    write_files([TEST_LOCATION], [], [], tmp_path.as_posix())

    content = (tmp_path / "Constants.java").read_text()
    assert 'public static final String DARK_CAVE_NAME = "dark cave";' in content
    assert 'public static final String DARK_CAVE_SHORT_DESCRIPTION = "dark cave short description";' in content
    assert 'public static final String DARK_CAVE_LONG_DESCRIPTION = "dark cave long description";' in content

def test_single_item_constants(tmp_path):
    write_files([], [], [TEST_ITEM], tmp_path.as_posix())

    content = (tmp_path / "Constants.java").read_text()
    assert 'public static final String KEY_NAME = "key";' in content
    assert 'public static final String KEY_INVENTORY_DESCRIPTION = "key inventory description";' in content
    assert 'public static final String KEY_LOCATION_DESCRIPTION = "key location description";' in content
    assert 'public static final String KEY_DETAILED_DESCRIPTION = "key detailed description";' in content
    assert 'public static final Set<String> KEY_ALIASES = Set.of("key ring");' in content

def test_multiple_aliases_item_constants(tmp_path):
    item = Item(name="rope",
                inventory_description="rope inventory description",
                location_description="rope location description",
                detailed_description="rope detailed description",
                aliases=["rope", "cord", "string"],
                location="barn")
    write_files([], [], [item], tmp_path.as_posix())

    content = (tmp_path / "Constants.java").read_text()
    assert 'public static final Set<String> ROPE_ALIASES = Set.of("rope", "cord", "string");' in content

def test_add_location(tmp_path):
    write_files([TEST_LOCATION], [], [], tmp_path.as_posix())
    content = (tmp_path / "map.txt").read_text()
    expected = """
.addLocation(new Location(
  Constants.DARK_CAVE_NAME,
  Constants.DARK_CAVE_LONG_DESCRIPTION,
  Constants.DARK_CAVE_SHORT_DESCRIPTION))"""

    assert expected in content

def test_add_item(tmp_path):
    write_files([], [], [TEST_ITEM], tmp_path.as_posix())
    content = (tmp_path / "map.txt").read_text()
    expected = """
.placeItem(new Item(
  Constants.KEY_NAME,
  Constants.KEY_INVENTORY_DESCRIPTION,
  Constants.KEY_LOCATION_DESCRIPTION,
  Constants.KEY_DETAILED_DESCRIPTION,
  Constants.KEY_ALIASES),
  Constants.DARK_CAVE_NAME))"""

    assert expected in content

def test_connect_locations(tmp_path):
    target_location = Location(
        name="hall of the mountain king",
        short_description="hall of the mountain king short description",
        long_description="hall of the mountain king long description",
    )
    connection = Connection(
        source_location=TEST_LOCATION.name,
        target_location=target_location.name,
        direction="NORTH")
    write_files([TEST_LOCATION, target_location],[connection], [], tmp_path.as_posix())
    content = (tmp_path / "map.txt").read_text()

    expected = ".connectOneWay(Constants.DARK_CAVE_NAME, Direction.NORTH, Constants.HALL_OF_THE_MOUNTAIN_KING_NAME)"
    assert expected in content
