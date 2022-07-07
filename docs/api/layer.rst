.. _layer_api:
Layer
=====

This module provides classes for all layer types

There is the base Layer class, which TileLayer, ObjectLayer, ImageLayer, 
and LayerGroup all derive from. The base Layer class is never directly used,
and serves only as an abstract base for common elements between all types.

For more information about Layers, see `Tiled's Manual <https://doc.mapeditor.org/en/stable/manual/layers/>`_


pytiled_parser.Layer
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pytiled_parser.Layer
    :members:

pytiled_parser.TileLayer
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pytiled_parser.TileLayer
    :members:

pytiled_parser.Chunk
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pytiled_parser.Chunk
    :members:

pytiled_parser.ObjectLayer
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pytiled_parser.ObjectLayer
    :members:

pytiled_parser.ImageLayer
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pytiled_parser.ImageLayer
    :members:

pytiled_parser.LayerGroup
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pytiled_parser.LayerGroup
    :members: