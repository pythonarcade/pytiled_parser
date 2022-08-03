.. _parser_api:
Parser
======

This module exposes the actual parsing functions. If you are creating an implementation, this is
what you will actually pass a file to and receive back a PyTiled Parser Map or World class depending
on what you're parsing.

pytiled_parser.parse_map
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pytiled_parser.parse_map

pytiled_parser.parse_world
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pytiled_parser.parse_world