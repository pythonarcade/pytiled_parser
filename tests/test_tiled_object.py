"""Tests for objects"""
import xml.etree.ElementTree as etree
from contextlib import ExitStack as does_not_raise

import pytest

from pytiled_parser import common_types, tiled_object

ELLIPSES = []

RECTANGLES = [
    (
        """
        {
        "height":41.4686825053996,
        "id":1,
        "name":"name: rectangle",
        "rotation":0,
        "type":"rectangle",
        "visible":true,
        "width":45.3972945322269,
        "x":27.7185404115039,
        "y":23.571672160964
        }
        """,
        tiled_object.Rectangle(
            id_=1,
            size=common_types.Size(45.3972945322269, 41.4686825053996),
            name="name: rectangle",
            rotation=0,
            type="rectangle",
            visible=True,
            coordinates=common_types.OrderedPair(27.7185404115039, 23.571672160964),
        ),
    ),
]

POINTS = [
    (
        """
        {
        "height":0,
        "id":2,
        "name":"name:  point",
        "point":true,
        "rotation":0,
        "type":"point",
        "visible":true,
        "width":0,
        "x":159.981811981357,
        "y":82.9373650107991
        }
        """,
        {
            "height": 0,
            "id": 2,
            "name": "name:  point",
            "point": True,
            "rotation": 0,
            "type": "point",
            "visible": True,
            "width": 0,
            "x": 159.981811981357,
            "y": 82.9373650107991,
        },
    ),
]

TILE_IMAGES = []

POLYGONS = []

POLYLINES = []

TEXTS = []

OBJECTS = ELLIPSES + RECTANGLES + POINTS + TILE_IMAGES + POLYGONS + POLYLINES + TEXTS


@pytest.mark.parametrize("raw_object,expected", OBJECTS)
def test_parse_layer(raw_object, expected):
    result = tiled_object._cast_tiled_object(raw_object)

    assert result == expected
