.. _properties_api:
Properties
==========

This module provides some common types used throughout PyTiled Parser. These are all just NamedTuple 
classes provided to make sets of data more clear. As such they can be subscripted like a normal tuple
to get the same values, or you can reference them by name. The values shown here are in the order they
will be in the final tuple.

Properties do not have a special class or anything associated with them. They are simply type aliases for
built-in Python types.

pytiled_parser.Property
^^^^^^^^^^^^^^^^^^^^^^^

The ``pytiled_parser.Property`` type is a Union of the `float`, `str`, and `bool` built-in types, as well as
`Path` class from pathlib, and the `pytiled_parser.Color` common type.

A property may be any one of these types.

pytiled_parser.Properties
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pytiled_parser.Properties`` type is a Dictionary mapping of `str` to `pytiled_parser.Property` objects.

When the map is parsed, all properties will be loaded in as a Property, and stored in a Properties dictionary
with the name being it's key in the dictionary.
