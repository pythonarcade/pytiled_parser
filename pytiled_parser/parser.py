from pathlib import Path

from pytiled_parser.parsers.json.tiled_map import parse as json_map_parse
from pytiled_parser.parsers.tmx.tiled_map import parse as tmx_map_parse
from pytiled_parser.tiled_map import TiledMap


def parse_map(file: Path) -> TiledMap:
    """Parse the raw Tiled map into a pytiled_parser type

    Args:
        file: Path to the map's JSON file

    Returns:
        TileSet: a properly typed TileSet.
    """
    # I have no idea why, but mypy thinks this function returns "Any"
    return json_map_parse(file)  # type: ignore


def parse_tmx(file: Path) -> TiledMap:
    return tmx_map_parse(file)  # type: ignore
