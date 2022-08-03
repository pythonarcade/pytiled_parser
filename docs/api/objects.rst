.. _objects_api:
Objects
=======

This module provides classes for all of the Tiled Object types.

There is the base TiledObject class, which all of the actual object types inherit from.
The base TiledObject class is never directly used, and serves only as an abstract base
for common elements between all types.

Some objects have no extra attributes over the base class, they exist as different classes anyways
to denote the type of object, so that an implementation can load it in accordingly. For example, an
Ellipse and a Point have no differing attributes from the base class, but obviously need to be handled
very differently.

For more information about objects, see `Tiled's Manual <https://doc.mapeditor.org/en/stable/manual/objects/>`_

Also see the `TMX Reference <https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#object>`_
and `JSON Reference <https://doc.mapeditor.org/en/stable/reference/json-map-format/#object>`_

TiledObject
^^^^^^^^^^^

.. autoclass:: pytiled_parser.tiled_object.TiledObject

Ellipse
^^^^^^^

.. autoclass:: pytiled_parser.tiled_object.Ellipse

Point
^^^^^

.. autoclass:: pytiled_parser.tiled_object.Point

Polygon
^^^^^^^

.. autoclass:: pytiled_parser.tiled_object.Polygon

Polyline
^^^^^^^^

.. autoclass:: pytiled_parser.tiled_object.Polyline

Rectangle
^^^^^^^^^

.. autoclass:: pytiled_parser.tiled_object.Rectangle

Text
^^^^

.. autoclass:: pytiled_parser.tiled_object.Text

Tile
^^^^

.. autoclass:: pytiled_parser.tiled_object.Tile