.. _api:
Programming Guide
=================

This section will guide you through the implementation details of using PyTiled Parser. This is not
an exact science, and will depend heavily on the library you are trying to integrate with. A lot of
the techniques here will show some general concepts and sort of pseudo code, as well as compare to the
`Arcade <https://api.arcade.academy/>`_ implementation as it is the most complete implementation of this
library to date.

Many liberties are taken when implementing with a game engine to suit that engines needs specifically. It
is a double edged sword of using Tiled, it is very flexible and can be implemented in a lot of different ways.
This comes at the cost of making a guide like this not as straight forward as it otherwise would be.

.. toctree::
    :maxdepth: 1

    map_loading
