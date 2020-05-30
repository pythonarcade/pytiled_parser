"""Helper unitilies for pytiled_parser."""

from typing import List, Optional

import pytiled_parser.objects as objects


def parse_color(color: str) -> objects.Color:
    """Convert Tiled color format into Arcade's.

    Args:
        color (str): Tiled formatted color string.

    Returns:
        :Color: Color object in the format that Arcade understands.
    """
    # the actual part we care about is always an even number
    if len(color) % 2:
        # strip initial '#' character
        color = color[1:]

    if len(color) == 6:
        # full opacity if no alpha specified
        alpha = 0xFF
        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)
    else:
        alpha = int(color[0:2], 16)
        red = int(color[2:4], 16)
        green = int(color[4:6], 16)
        blue = int(color[6:8], 16)

    return objects.Color(red, green, blue, alpha)


def _get_tile_set_key(gid: int, tile_set_keys: List[int]) -> int:
    """Gets tile set key given a tile GID.

    Args:
        gid (int): Global ID of the tile.
        tile_set_keys (List[int]): List of tile set keys.

    Returns:
        int: The key of the tile set that contains the tile for the GID.
    """

    # credit to __m4ch1n3__ on ##learnpython for this idea
    return max([key for key in tile_set_keys if key <= gid])


def get_tile_by_gid(gid: int, tile_sets: objects.TileSetDict) -> Optional[objects.Tile]:
    """Gets correct Tile for a given global ID.

    Args:
        tile_sets (objects.TileSetDict): TileSetDict from TileMap.
        gid (int): Global tile ID of the tile to be returned.

    Returns:
        objects.Tile: The Tile object reffered to by the global tile ID.
        None: If there is no objects.Tile object in the tile_set.tiles dict for the associated gid.
    """
    tile_set_key = _get_tile_set_key(gid, list(tile_sets.keys()))
    tile_set = tile_sets[tile_set_key]

    if tile_set.tiles is not None:
        return tile_set.tiles.get(gid - tile_set_key)

    return None
