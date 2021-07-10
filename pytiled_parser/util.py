"""Utility Functions for PyTiled"""

from pytiled_parser.common_types import Color


def parse_color(color: str) -> Color:
    """Convert Tiled color format into PyTiled's.
    Args:
        color (str): Tiled formatted color string.
    Returns:
        :Color: Color object in the format that PyTiled understands.
    """
    # the actual part we care about is always an even number
    if len(color) % 2:
        # strip initial '#' character
        color = color[1:]

    if len(color) == 6:
        # full opacity if no alpha specified
        return Color(int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), 255)
    elif len(color) == 8:
        return Color(
            int(color[2:4], 16),
            int(color[4:6], 16),
            int(color[6:8], 16),
            int(color[0:2], 16),
        )

    raise ValueError("Improperly formatted color passed to parse_color")
