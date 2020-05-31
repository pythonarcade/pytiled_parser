"""Tests for objects"""
from contextlib import ExitStack as does_not_raise
from pathlib import Path

import pytest

from pytiled_parser import common_types, tiled_object

ELLIPSES = [
    (
        """
        {
        "ellipse":true,
        "height":18.5517790155735,
        "id":6,
        "name":"name: ellipse",
        "rotation":0,
        "type":"ellipse",
        "visible":true,
        "width":57.4013868364215,
        "x":37.5400704785722,
        "y":81.1913152210981
        }
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
        {
        "ellipse":true,
        "height":31.4288962146186,
        "id":7,
        "name":"name: ellipse - invisible",
        "rotation":0,
        "type":"ellipse",
        "visible":false,
        "width":6.32943048766625,
        "x":22.6986472661134,
        "y":53.9092872570194
        }
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
        {
        "ellipse":true,
        "height":24.2264408321018,
        "id":8,
        "name":"name: ellipse - rotated",
        "rotation":111,
        "type":"ellipse",
        "visible":true,
        "width":29.6828464249176,
        "x":35.7940206888712,
        "y":120.040923041946
        }
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

POLYLINES = [
    (
        """
        {
        "height":0,
        "id":9,
        "name":"name: polyline",
        "polygon":[
            {
                "x":0,
                "y":0
            },
            {
                "x":19.424803910424,
                "y":27.063771740366
            },
            {
                "x":19.6430601341366,
                "y":3.05558713197681
            },
            {
                "x":-2.61907468455156,
                "y":15.9327043310219
            },
            {
                "x":25.317721950665,
                "y":16.3692167784472
            }],
        "rotation":0,
        "type":"polyline",
        "visible":true,
        "width":0,
        "x":89.485051722178,
        "y":38.6313515971354
        }
        """,
        tiled_object.Polyline(
            id_=9,
            name="name: polyline",
            points=[
                common_types.OrderedPair(0, 0),
                common_types.OrderedPair(19.424803910424, 27.063771740366),
                common_types.OrderedPair(19.6430601341366, 3.05558713197681),
                common_types.OrderedPair(-2.61907468455156, 15.9327043310219),
                common_types.OrderedPair(25.317721950665, 16.3692167784472),
            ],
            rotation=0,
            type="polyline",
            visible=True,
            coordinates=common_types.OrderedPair(89.485051722178, 38.6313515971354),
        ),
    ),
    (
        """
        {
                 "height":0,
                 "id":10,
                 "name":"name: polyline - invisible",
                 "polygon":[
                        {
                         "x":0,
                         "y":0
                        },
                        {
                         "x":-12.8771171990451,
                         "y":7.63896782994203
                        },
                        {
                         "x":-14.8414232124588,
                         "y":-10.2580425144936
                        }],
                 "rotation":0,
                 "type":"polyline",
                 "visible":false,
                 "width":0,
                 "x":133.791065135842,
                 "y":24.4446970558145
        }
        """,
        tiled_object.Polyline(
            id_=10,
            name="name: polyline - invisible",
            points=[
                common_types.OrderedPair(0, 0),
                common_types.OrderedPair(-12.8771171990451, 7.63896782994203),
                common_types.OrderedPair(-14.8414232124588, -10.2580425144936),
            ],
            rotation=0,
            type="polyline",
            visible=False,
            coordinates=common_types.OrderedPair(133.791065135842, 24.4446970558145),
        ),
    ),
    (
        """
        {
                 "height":0,
                 "id":11,
                 "name":"name: polyline - rotated",
                 "polygon":[
                        {
                         "x":0,
                         "y":0
                        },
                        {
                         "x":-12.8771171990451,
                         "y":0
                        },
                        {
                         "x":-6.98419915880413,
                         "y":7.63896782994203
                        },
                        {
                         "x":-13.9683983176083,
                         "y":16.8057292258725
                        },
                        {
                         "x":3.71035580311468,
                         "y":15.277935659884
                        },
                        {
                         "x":-3.71035580311471,
                         "y":8.29373650107991
                        }],
                 "rotation":123,
                 "type":"polyline",
                 "visible":true,
                 "width":0,
                 "x":152.779356598841,
                 "y":19.8613163578493
        }
        """,
        tiled_object.Polyline(
            id_=11,
            name="name: polyline - rotated",
            points=[
                common_types.OrderedPair(0, 0),
                common_types.OrderedPair(-12.8771171990451, 0),
                common_types.OrderedPair(-6.98419915880413, 7.63896782994203),
                common_types.OrderedPair(-13.9683983176083, 16.8057292258725),
                common_types.OrderedPair(3.71035580311468, 15.277935659884),
                common_types.OrderedPair(-3.71035580311471, 8.29373650107991),
            ],
            rotation=123,
            type="polyline",
            visible=True,
            coordinates=common_types.OrderedPair(152.779356598841, 19.8613163578493),
        ),
    ),
    (
        """
        {
                 "height":0,
                 "id":12,
                 "name":"name: polyline - not closed",
                 "polyline":[
                        {
                         "x":0,
                         "y":0
                        },
                        {
                         "x":-13.3136296464704,
                         "y":41.0321700579743
                        },
                        {
                         "x":21.3891099238377,
                         "y":16.8057292258725
                        }],
                 "rotation":0,
                 "type":"polyline",
                 "visible":true,
                 "width":0,
                 "x":124.187791292486,
                 "y":90.1398203933159
        }
        """,
        tiled_object.Polyline(
            id_=12,
            name="name: polyline - not closed",
            points=[
                common_types.OrderedPair(0, 0),
                common_types.OrderedPair(-13.3136296464704, 41.0321700579743),
                common_types.OrderedPair(21.3891099238377, 16.8057292258725),
            ],
            rotation=0,
            type="polyline",
            visible=True,
            coordinates=common_types.OrderedPair(124.187791292486, 90.1398203933159),
        ),
    ),
]

TEXTS = []

OBJECTS = ELLIPSES + RECTANGLES + POINTS + TILE_IMAGES + POLYGONS + POLYLINES + TEXTS


@pytest.mark.parametrize("raw_object,expected", OBJECTS)
def test_parse_layer(raw_object, expected):
    result = tiled_object._cast_tiled_object(raw_object)

    assert result == expected
