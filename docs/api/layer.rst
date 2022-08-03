.. _layer_api:
Layer
=====

This module provides classes for all layer types

There is the base Layer class, which TileLayer, ObjectLayer, ImageLayer, 
and LayerGroup all derive from. The base Layer class is never directly used,
and serves only as an abstract base for common elements between all types.

For more information about Layers, see `Tiled's Manual <https://doc.mapeditor.org/en/stable/manual/layers/>`_


Layer
^^^^^

.. autoclass:: pytiled_parser.layer.Layer
    :members:

TileLayer
^^^^^^^^^

.. autoclass:: pytiled_parser.layer.TileLayer
    :members:

Chunk
^^^^^

.. autoclass:: pytiled_parser.layer.Chunk
    :members:

ObjectLayer
^^^^^^^^^^^

.. autoclass:: pytiled_parser.layer.ObjectLayer
    :members:

ImageLayer
^^^^^^^^^^

.. autoclass:: pytiled_parser.layer.ImageLayer
    :members:

LayerGroup
^^^^^^^^^^

.. autoclass:: pytiled_parser.layer.LayerGroup
    :members: