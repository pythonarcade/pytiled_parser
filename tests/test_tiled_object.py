"""Tests for objects"""
import xml.etree.ElementTree as etree
from contextlib import ExitStack as does_not_raise

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
        tiled_object.Point(
            id_=2,
            name="name:  point",
            rotation=0,
            type="point",
            visible=True,
            coordinates=common_types.OrderedPair(159.981811981357, 82.9373650107991),
        ),
    ),
    (
        """
        {
                 "height":0,
                 "id":3,
                 "name":"name:  point invisible",
                 "point":true,
                 "rotation":0,
                 "type":"point",
                 "visible":false,
                 "width":0,
                 "x":109.346368080027,
                 "y":95.8144822098443
        }
        """,
        tiled_object.Point(
            id_=3,
            name="name:name:  point invisible",
            rotation=0,
            type="point",
            visible=True,
            coordinates=common_types.OrderedPair(109.346368080027, 95.8144822098443),
        ),
    ),
]

TILE_IMAGES = []

POLYGONS = [
    (
        """
        {
                 "height":0,
                 "id":9,
                 "name":"name: polygon",
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
                 "type":"polygon",
                 "visible":true,
                 "width":0,
                 "x":89.485051722178,
                 "y":38.6313515971354
        }
        """,
        tiled_object.Polygon(
            id_=9,
            name="name: polygon",
            points=[
                common_types.OrderedPair(0, 0),
                common_types.OrderedPair(19.424803910424, 27.063771740366),
                common_types.OrderedPair(19.6430601341366, 3.05558713197681),
                common_types.OrderedPair(-2.61907468455156, 15.9327043310219),
                common_types.OrderedPair(25.317721950665, 16.3692167784472),
            ],
            rotation=0,
            type="polygon",
            visible=True,
            coordinates=common_types.OrderedPair(89.485051722178, 38.6313515971354),
        ),
    ),
    (
        """
        {
                 "height":0,
                 "id":10,
                 "name":"name: polygon - invisible",
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
                 "type":"polygon",
                 "visible":false,
                 "width":0,
                 "x":133.791065135842,
                 "y":24.4446970558145
        }
        """,
        tiled_object.Polygon(
            id_=9,
            name="name: polygon - invisible",
            points=[
                common_types.OrderedPair(0, 0),
                common_types.OrderedPair(-12.8771171990451, 7.63896782994203),
                common_types.OrderedPair(-14.8414232124588, -10.2580425144936),
            ],
            rotation=0,
            type="polygon",
            visible=False,
            coordinates=common_types.OrderedPair(133.791065135842, 24.4446970558145),
        ),
    ),
    (
        """
        {
                 "height":0,
                 "id":11,
                 "name":"name: polygon - rotated",
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
                 "type":"polygon",
                 "visible":true,
                 "width":0,
                 "x":152.779356598841,
                 "y":19.8613163578493
        }
        """,
        tiled_object.Polygon(
            id_=9,
            name="name: polygon - rotated",
            points=[
                common_types.OrderedPair(0, 0),
                common_types.OrderedPair(-12.8771171990451, 0),
                common_types.OrderedPair(-6.98419915880413, 7.63896782994203),
                common_types.OrderedPair(-13.9683983176083, 16.8057292258725),
                common_types.OrderedPair(3.71035580311468, 15.277935659884),
                common_types.OrderedPair(-3.71035580311471, 8.29373650107991),
            ],
            rotation=123,
            type="polygon",
            visible=True,
            coordinates=common_types.OrderedPair(152.779356598841, 19.8613163578493),
        ),
    ),
]

POLYLINES = [
    (
        """
        {
                 "height":0,
                 "id":12,
                 "name":"name: polyline",
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
            id_=9,
            name="name: polyline",
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
    (
        """
        {
                 "height":0,
                 "id":31,
                 "name":"name: polyline - invisible",
                 "polyline":[
                        {
                         "x":0,
                         "y":0
                        },
                        {
                         "x":-9,
                         "y":20.3333333333333
                        },
                        {
                         "x":5,
                         "y":23.6666666666667
                        }],
                 "rotation":0,
                 "type":"polyline",
                 "visible":false,
                 "width":0,
                 "x":140,
                 "y":163.333333333333
        }
        """,
        tiled_object.Polyline(
            id_=10,
            name="name: polyline - invisible",
            points=[
                common_types.OrderedPair(0, 0),
                common_types.OrderedPair(-9, 20.3333333333333),
                common_types.OrderedPair(5, 23.6666666666667),
            ],
            rotation=0,
            type="polyline",
            visible=False,
            coordinates=common_types.OrderedPair(140, 163.333333333333),
        ),
    ),
    (
        """
        {
                 "height":0,
                 "id":32,
                 "name":"name: polyline - rotated",
                 "polyline":[
                        {
                         "x":0,
                         "y":0
                        },
                        {
                         "x":10.3333333333333,
                         "y":13
                        },
                        {
                         "x":-5.33333333333331,
                         "y":19.6666666666667
                        }],
                 "rotation":0,
                 "type":"polyline",
                 "visible":true,
                 "width":0,
                 "x":192.333333333333,
                 "y":128.666666666667
        }
        """,
        tiled_object.Polyline(
            id_=11,
            name="name: polyline - rotated",
            points=[
                common_types.OrderedPair(0, 0),
                common_types.OrderedPair(10.3333333333333, 13),
                common_types.OrderedPair(-5.33333333333331, 19.6666666666667),
            ],
            rotation=0,
            type="polyline",
            visible=True,
            coordinates=common_types.OrderedPair(192.333333333333, 128.666666666667),
        ),
    ),
]

TEXTS = []

OBJECTS = ELLIPSES + RECTANGLES + POINTS + TILE_IMAGES + POLYGONS + POLYLINES + TEXTS


@pytest.mark.parametrize("raw_object,expected", OBJECTS)
def test_parse_layer(raw_object, expected):
    result = tiled_object._cast_tiled_object(raw_object)

    assert result == expected
