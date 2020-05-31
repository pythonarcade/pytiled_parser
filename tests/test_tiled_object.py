"""Tests for objects"""
import xml.etree.ElementTree as etree
from contextlib import ExitStack as does_not_raise
from pathlib import Path

import pytest

from pytiled_parser import common_types, properties, tiled_object

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
    (
        """
        {
        "height":32.7384335568944,
        "id":4,
        "name":"name:  rectangle - invisible",
        "rotation":0,
        "type":"rectangle",
        "visible":false,
        "width":30.9923837671934,
        "x":163.910424008185,
        "y":91.0128452881664
        }
        """,
        tiled_object.Rectangle(
            id_=4,
            size=common_types.Size(30.9923837671934, 32.7384335568944),
            name="name:  rectangle - invisible",
            rotation=0,
            type="rectangle",
            visible=False,
            coordinates=common_types.OrderedPair(163.910424008185, 91.0128452881664),
        ),
    ),
    (
        """
        {
        "height":22,
        "id":5,
        "name":"name:  rectangle - rotated",
        "rotation":10,
        "type":"rectangle",
        "visible":true,
        "width":10,
        "x":183.335227918609,
        "y":23.3534159372513
        },
        """,
        tiled_object.Rectangle(
            id_=5,
            size=common_types.Size(10, 22),
            name="name:  rectangle - rotated",
            rotation=10,
            type="rectangle",
            visible=True,
            coordinates=common_types.OrderedPair(183.335227918609, 23.3534159372513),
        ),
    ),
    (
        """
        {
        "height":0,
        "id":28,
        "name":"name: rectangle - no width or height",
        "rotation":0,
        "type":"rectangle",
        "visible":true,
        "width":0,
        "x":131.17199045129,
        "y":53.4727748095942
        }
        """,
        tiled_object.Rectangle(
            id_=28,
            size=common_types.Size(0, 0),
            name="name: rectangle - no width or height",
            rotation=0,
            type="rectangle",
            visible=True,
            coordinates=common_types.OrderedPair(131.17199045129, 53.4727748095942),
        ),
    ),
    (
        r"""
        {
         "height":13.7501420938956,
         "id":30,
         "name":"name: rectangle - properties",
         "properties":[
                {
                 "name":"bool property",
                 "type":"bool",
                 "value":false
                },
                {
                 "name":"color property",
                 "type":"color",
                 "value":"#ffaa0000"
                },
                {
                 "name":"file property",
                 "type":"file",
                 "value":"..\/..\/..\/..\/..\/..\/dev\/null"
                },
                {
                 "name":"float property",
                 "type":"float",
                 "value":42.1
                },
                {
                 "name":"int property",
                 "type":"int",
                 "value":8675309
                },
                {
                 "name":"string property",
                 "type":"string",
                 "value":"pytiled_parser rulez!1!!"
                }],
         "rotation":0,
         "type":"rectangle",
         "visible":true,
         "width":21.170853700125,
         "x":39.0678640445606,
         "y":131.826759122428
        }
        """,
        tiled_object.Rectangle(
            id_=30,
            size=common_types.Size(21.170853700125, 13.7501420938956),
            name="name: rectangle - properties",
            rotation=0,
            type="rectangle",
            visible=True,
            coordinates=common_types.OrderedPair(39.0678640445606, 131.826759122428),
            properties={
                "bool property": False,
                "color property": "#ffaa0000",
                "file property": Path("../../../../../../dev/null"),
                "float property": 42.1,
                "int property": 8675309,
                "string property": "pytiled_parser rulez!1!!",
            },
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
