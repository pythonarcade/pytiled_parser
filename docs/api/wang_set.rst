.. _wang_set_api:
Wang Set
========

This module contains a number of classes related to Wang Sets.

Wang Sets are the underlying data used by Tiled's terrain system. It is unlikely this module will
ever need touched for creating an implementation in a game engine. It is primarily data used by the
editor during map creation.

See `Tiled's docs about terrain <https://doc.mapeditor.org/en/stable/manual/terrain/>`_
and also the `TMX Reference <https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#wangsets>`_
and the `JSON Reference <https://doc.mapeditor.org/en/stable/reference/json-map-format/#wang-set>`_

WangSet
^^^^^^^

.. autoclass:: pytiled_parser.wang_set.WangSet

WangColor
^^^^^^^^^

.. autoclass:: pytiled_parser.wang_set.WangColor

WangTile
^^^^^^^^

.. autoclass:: pytiled_parser.wang_set.WangTile