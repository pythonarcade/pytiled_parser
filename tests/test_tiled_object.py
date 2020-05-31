"""Tests for objects"""
import xml.etree.ElementTree as etree
from contextlib import ExitStack as does_not_raise

import pytest

from pytiled_parser import common_types, tiled_object

ELLIPSES = [
    (
        """
        {"ellipse":true,
        "height":18.5517790155735,
        "id":6,
        "name":"name: ellipse",
        "rotation":0,
        "type":"ellipse",
        "visible":true,
        "width":57.4013868364215,
        "x":37.5400704785722,
        "y":81.1913152210981}
        """,
        tiled_object.Ellipse(
            id_=6,
            size=common_types.Size(57.4013868364215, 18.5517790155735),
            name="name: ellipse",
            rotation=0,
            type="ellipse",
            visible=True,
            coordinates=common_types.OrderedPair(37.5400704785722, 81.1913152210981),
        ),
    ),
    (
        """
        {"ellipse":true,
        "height":31.4288962146186,
        "id":7,
        "name":"name: ellipse - invisible",
        "rotation":0,
        "type":"ellipse",
        "visible":false,
        "width":6.32943048766625,
        "x":22.6986472661134,
        "y":53.9092872570194}
        """,
        tiled_object.Ellipse(
            id_=7,
            size=common_types.Size(6.32943048766625, 31.4288962146186),
            name="name: ellipse - invisible",
            rotation=0,
            type="ellipse",
            visible=True,
            coordinates=common_types.OrderedPair(22.6986472661134, 53.9092872570194),
        ),
    ),
    (
        """
        {"ellipse":true,
        "height":24.2264408321018,
        "id":8,
        "name":"name: ellipse - rotated",
        "rotation":111,
        "type":"ellipse",
        "visible":true,
        "width":29.6828464249176,
        "x":35.7940206888712,
        "y":120.040923041946}
        """,
        tiled_object.Ellipse(
            id_=8,
            size=common_types.Size(29.6828464249176, 24.2264408321018),
            name="name: ellipse - rotated",
            rotation=111,
            type="ellipse",
            visible=True,
            coordinates=common_types.OrderedPair(35.7940206888712, 120.040923041946),
        ),
    ),
]

RECTANGLES = [
    (
        """
        {"height":41.4686825053996,
        "id":1,
        "name":"name: rectangle",
        "rotation":0,
        "type":"rectangle",
        "visible":true,
        "width":45.3972945322269,
        "x":27.7185404115039,
        "y":23.571672160964}
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
        {"height":0,
        "id":2,
        "name":"name:  point",
        "point":true,
        "rotation":0,
        "type":"point",
        "visible":true,
        "width":0,
        "x":159.981811981357,
        "y":82.9373650107991}
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
