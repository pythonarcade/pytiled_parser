PyTiled Parser
==============

PyTiled Parser is a Python Library for parsing `Tiled Map Editor <https://www.mapeditor.org/>`_ maps and tilesets
to be used as maps and levels for 2D games in a strictly typed fashion.

PyTiled Parser is not tied to any particular graphics library or game engine. It parses map files and returns arbitrary
Python types(for example, ``Path`` objects for image files rather than a ``Sprite`` from a specific engine). This means
it can be used to aide in implementing Tiled support into a wide variety of tools.

* Documentation available at: https://pytiled-parser.readthedocs.io/
* GitHub Project: https://github.com/pythonarcade/pytiled_parser
* PyPi: https://pypi.org/project/pytiled-parser/

The `Arcade <https://api.arcade.academy/>`_ library has `supporting code <https://api.arcade.academy/en/latest/api/tilemap.html>`_
to integrate PyTiled Parser, as well as `example code <https://api.arcade.academy/en/latest/examples/index.html#using-tiled-map-editor-to-create-maps>`_
showing it's use.

Installation
^^^^^^^^^^^^

Simply install with pip::

   pip install pytiled-parser

Quick Links
^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   guide/index
   api/index



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
