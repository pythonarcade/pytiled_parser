.. _world_api:
World
=====

This module provides an implementation for the World files from Tiled.

See `Tiled's docs for Worlds <https://doc.mapeditor.org/en/stable/manual/worlds/>`_
for more info about worlds and what they do.

The functionality within PyTiled Parser is to load the world and outline the size
and position of each map, and provide the path to the map file. Loading a world
does not automatically load each map within the world, this is so that the game
or engine implementation can decide how to handle map loading.

WorldMap
^^^^^^^^

.. autoclass:: pytiled_parser.world.WorldMap

World
^^^^^

.. autoclass:: pytiled_parser.world.World