from pathlib import Path

from pytiled_parser import UnknownFormat
from pytiled_parser.parsers.json.tiled_map import parse as json_map_parse
from pytiled_parser.parsers.tmx.tiled_map import parse as tmx_map_parse
from pytiled_parser.tiled_map import TiledMap
from pytiled_parser.util import check_format
from pytiled_parser.world import World
from pytiled_parser.world import parse_world as _parse_world


def parse_map(file: Path) -> TiledMap:
    """Parse the raw Tiled map into a pytiled_parser type

    Args:
        file: Path to the map file

    Returns:
        TiledMap: A parsed and typed TiledMap
    """
    parser = check_format(file)

    # The type ignores are because mypy for some reason thinks those functions return Any
    if parser == "tmx":
        return tmx_map_parse(file)  # type: ignore
    else:
        try:
            return json_map_parse(file)  # type: ignore
        except ValueError:
            raise UnknownFormat(
                "Unknown Map Format, please use either the TMX or JSON format. "
                "This message could also mean your map file is invalid or corrupted."
            )


def parse_world(file: Path) -> World:
    """Parse the raw world file into a pytiled_parser type

    Args:
        file: Path to the world file

    Returns:
        World: A parsed and typed World
    """
    return _parse_world(file)
