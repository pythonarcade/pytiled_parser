"""Handle XML parsing for TMX files"""

import base64
import functools
import gzip
import re
import xml.etree.ElementTree as etree
import zlib
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union

import pytiled_parser.objects as objects
from pytiled_parser.utilities import parse_color

def _decode_base64_data(
    data_text: str, layer_width: int, compression: Optional[str] = None
) -> List[List[int]]:
    """Decode base64 data.

    Args:
        data_text (str): Data to be decoded.
        layer_width (int): Width of each layer in tiles.
        compression (Optional[str]): The type of compression for the data.

    Raises:
        ValueError: If compression type is unsupported.

    Returns:
        :List[List[int]]: Tile grid.
    """
    tile_grid: List[List[int]] = [[]]

    unencoded_data = base64.b64decode(data_text)
    if compression == "zlib":
        unzipped_data = zlib.decompress(unencoded_data)
    elif compression == "gzip":
        unzipped_data = gzip.decompress(unencoded_data)
    elif compression is None:
        unzipped_data = unencoded_data
    else:
        raise ValueError(f"Unsupported compression type '{compression}'.")

    # Turn bytes into 4-byte integers
    byte_count = 0
    int_count = 0
    int_value = 0
    row_count = 0
    for byte in unzipped_data:
        int_value += byte << (byte_count * 8)
        byte_count += 1
        if not byte_count % 4:
            byte_count = 0
            int_count += 1
            tile_grid[row_count].append(int_value)
            int_value = 0
            if not int_count % layer_width:
                row_count += 1
                tile_grid.append([])

    tile_grid.pop()
    return tile_grid


def _decode_csv_data(data_text: str) -> List[List[int]]:
    """Decodes csv encoded layer data.

    Args:
        data_text (str): Data to be decoded.

    Returns:
        List[List[int]]: Tile grid.
    """
    tile_grid = []
    lines: List[str] = data_text.split("\n")
    # remove erroneous empty lists due to a newline being on both ends of text
    lines = lines[1:-1]
    for line in lines:
        line_list = line.split(",")
        # FIXME: what is this for?
        while "" in line_list:
            line_list.remove("")
        line_list_int = [int(item) for item in line_list]
        tile_grid.append(line_list_int)

    return tile_grid


def _decode_data(
    element: etree.Element,
    layer_width: int,
    encoding: str,
    compression: Optional[str] = None,
) -> List[List[int]]:
    """Decodes data or chunk data.

    Args:
        element (Element): Element to have text decoded.
        layer_width (int): Number of tiles per column in this layer. Used
            for determining when to cut off a row when decoding base64
            encoding layers.
        encoding (str): Encoding format of the layer data.
        compression (str): Compression format of the layer data.

    Raises:
        ValueError: Encoding type is not supported.
        ValueError: Compression is not supported for this encoding type.
        ValueError: Compression type is not supported
        AttributeError: No data in element.

    Returns:
        List[List[int]]: Tile grid.
    """
    # etree.Element.text comes with an appended and a prepended '\n'
    supported_encodings = ["base64", "csv"]
    if encoding not in supported_encodings:
        raise ValueError(f"{encoding} is not a supported encoding")

    supported_compression = [None, "gzip", "zlib"]
    if compression is not None:
        if encoding != "base64":
            raise ValueError(f"{encoding} does not support compression")
        if compression not in supported_compression:
            raise ValueError(f"{compression} is not a supported compression")

    try:
        data_text: str = element.text  # type: ignore
    except AttributeError:
        raise AttributeError(f"{element} lacks layer data.")

    if encoding == "csv":
        return _decode_csv_data(data_text)

    return _decode_base64_data(data_text, layer_width, compression)


def _parse_data(element: etree.Element, layer_width: int) -> objects.LayerData:
    """Parses layer data.

    Will parse CSV, base64, gzip-base64, or zlip-base64 encoded data.

    Args:
        element (Element): Data element to parse.
        layer_width (int): Layer width. Used for base64 decoding.

    Returns:
        LayerData: Data object containing layer data or chunks of data.
    """
    encoding = element.attrib["encoding"]
    compression = None
    try:
        compression = element.attrib["compression"]
    except KeyError:
        pass

    chunk_elements = element.findall("./chunk")
    if chunk_elements:
        chunks: List[objects.Chunk] = []
        for chunk_element in chunk_elements:
            x = int(chunk_element.attrib["x"])
            y = int(chunk_element.attrib["y"])
            location = objects.OrderedPair(x, y)
            width = int(chunk_element.attrib["width"])
            height = int(chunk_element.attrib["height"])
            layer_data = _decode_data(
                chunk_element, layer_width, encoding, compression
            )
            chunks.append(objects.Chunk(location, width, height, layer_data))
        return chunks

    return _decode_data(element, layer_width, encoding, compression)


def _parse_layer(
    layer_element: etree.Element
) -> Tuple[
    int,
    str,
    Optional[objects.OrderedPair],
    Optional[float],
    Optional[objects.Properties],
]:
    """Parses all of the attributes for a Layer object.

    Args:
        layer_element: The layer element to be parsed.

    Returns:
        FIXME
    """
    if "id" in layer_element:
        id_ = int(layer_element.attrib["id"])
    else:
        id_ = None

    name = layer_element.attrib["name"]

    offset: Optional[objects.OrderedPair]
    offset_x_attrib = layer_element.attrib.get("offsetx")
    offset_y_attrib = layer_element.attrib.get("offsety")
    # If any offset is present, we need to return an OrderedPair
    # Unknown if one of the offsets could be absent.
    if any([offset_x_attrib, offset_y_attrib]):
        if offset_x_attrib:
            offset_x = float(offset_x_attrib)
        else:
            offset_x = 0.0
        if offset_y_attrib:
            offset_y = float(offset_y_attrib)
        else:
            offset_y = 0.0

        offset = objects.OrderedPair(offset_x, offset_y)
    else:
        offset = None

    opacity: Optional[float]
    opacity_attrib = layer_element.attrib.get("opacity")
    if opacity_attrib:
        opacity = float(opacity_attrib)
    else:
        opacity = None

    properties: Optional[objects.Properties]
    properties_element = layer_element.find("./properties")
    if properties_element is not None:
        properties = _parse_properties_element(properties_element)
    else:
        properties = None

    return id_, name, offset, opacity, properties


def _parse_tile_layer(element: etree.Element,) -> objects.TileLayer:
    """Parses tile layer element.

    Args:
        element: The layer element to be parsed.

    Raises:
        ValueError: Element has no chile data element.

    Returns:
        TileLayer: The tile layer object.
    """
    id_, name, offset, opacity, properties = _parse_layer(element)

    width = int(element.attrib["width"])
    height = int(element.attrib["height"])
    size = objects.Size(width, height)

    data_element = element.find("./data")
    if data_element is not None:
        data: objects.LayerData = _parse_data(data_element, width)
    else:
        raise ValueError(f"{element} has no child data element.")

    return objects.TileLayer(
        id_=id_,
        name=name,
        offset=offset,
        opacity=opacity,
        properties=properties,
        size=size,
        data=data,
    )


def _parse_objects(
    object_elements: List[etree.Element]
) -> List[objects.TiledObject]:
    """Parses objects found in the 'objectgroup' element.

    Args:
        object_elements: List of object elements to be parsed.

    Returns:
        list: List of parsed tiled objects.
    """
    tiled_objects: List[objects.TiledObject] = []

    for object_element in object_elements:
        id_ = int(object_element.attrib["id"])
        location_x = float(object_element.attrib["x"])
        location_y = float(object_element.attrib["y"])
        location = objects.OrderedPair(location_x, location_y)

        tiled_object = objects.TiledObject(id_=id_, location=location)

        try:
            tiled_object.gid = int(object_element.attrib["gid"])
        except KeyError:
            tiled_object.gid = None

        try:
            width = float(object_element.attrib["width"])
        except KeyError:
            width = 0.0

        try:
            height = float(object_element.attrib["height"])
        except KeyError:
            height = 0.0

        tiled_object.size = objects.Size(width, height)

        try:
            tiled_object.opacity = float(object_element.attrib["opacity"])
        except KeyError:
            pass

        try:
            tiled_object.rotation = int(object_element.attrib["rotation"])
        except KeyError:
            pass

        try:
            tiled_object.name = object_element.attrib["name"]
        except KeyError:
            pass

        try:
            tiled_object.type = object_element.attrib["type"]
        except KeyError:
            pass

        properties_element = object_element.find("./properties")
        if properties_element is not None:
            tiled_object.properties = _parse_properties_element(
                properties_element
            )

        tiled_objects.append(tiled_object)

    return tiled_objects


def _parse_object_layer(element: etree.Element,) -> objects.ObjectLayer:
    """Parse the objectgroup element given.

    Args:
        element (etree.Element): Element to be parsed.

    Returns:
        ObjectLayer: The object layer object.
    """
    id_, name, offset, opacity, properties = _parse_layer(element)

    tiled_objects = _parse_objects(element.findall("./object"))

    color = None
    try:
        color = element.attrib["color"]
    except KeyError:
        pass

    draw_order = None
    try:
        draw_order = element.attrib["draworder"]
    except KeyError:
        pass

    return objects.ObjectLayer(
        id_=id_,
        name=name,
        offset=offset,
        opacity=opacity,
        properties=properties,
        tiled_objects=tiled_objects,
        color=color,
        draw_order=draw_order,
    )


def _parse_layer_group(element: etree.Element,) -> objects.LayerGroup:
    """Parse the objectgroup element given.

    Args:
        element (etree.Element): Element to be parsed.

    Returns:
        LayerGroup: The layer group object.
    """
    id_, name, offset, opacity, properties = _parse_layer(element)

    layers = _get_layers(element)

    return objects.LayerGroup(
        id_=id_,
        name=name,
        offset=offset,
        opacity=opacity,
        properties=properties,
        layers=layers,
    )


def _get_layer_parser(
    layer_tag: str
) -> Optional[Callable[[etree.Element], objects.Layer]]:
    """Gets a the parser for the layer type specified.

    Layer tags are 'layer' for a tile layer, 'objectgroup' for an object
        layer, and 'group' for a layer group. If anything else is passed,
        returns None.

    Args:
        layer_tag: Specifies the layer type to be parsed based on the element
            tag.

    Returns:
        Callable: the function to be used to parse the layer.
        None: The element is not a map layer.
    """
    if layer_tag == "layer":
        return _parse_tile_layer
    if layer_tag == "objectgroup":
        return _parse_object_layer
    if layer_tag == "group":
        return _parse_layer_group
    return None


def _get_layers(map_element: etree.Element) -> List[objects.Layer]:
    """Parse layer type element given.

    Retains draw order based on the returned lists index FIXME: confirm

    Args:
        map_element: The element containing the layer.

    Returns:
        List[Layer]: A list of the layers, ordered by draw order.
            FIXME: confirm
    """
    layers: List[objects.Layer] = []
    for element in map_element.findall("./"):
        layer_parser = _get_layer_parser(element.tag)
        if layer_parser:
            layers.append(layer_parser(element))

    return layers


@functools.lru_cache()
def _parse_external_tile_set(
    parent_dir: Path, tile_set_element: etree.Element
) -> objects.TileSet:
    """Parses an external tile set.

    Caches the results to speed up subsequent maps with identical tilesets.

    Args:
        parent_dir (Path): Directory that TMX is in.
        tile_set_element (etree.Element): Tile set element.

    Returns:
        objects.Tileset: The tileset being parsed.
    """
    source = Path(tile_set_element.attrib["source"])
    tile_set_tree = etree.parse(str(parent_dir / Path(source))).getroot()

    return _parse_tile_set(tile_set_tree)


def _parse_points(point_string: str) -> List[objects.OrderedPair]:
    str_pairs = point_string.split(" ")

    points = []
    for str_pair in str_pairs:
        xys = str_pair.split(",")
        x = float(xys[0])
        y = float(xys[1])
        points.append((x, y))

    return points


def _parse_tiles(
    tile_element_list: List[etree.Element]
) -> Dict[int, objects.Tile]:
    """Parse a list of tile elements.

    Args:
        tile_element_list (List[etree.Element]): List of tile elements.

    Returns:
        Dict[int, objects.Tile]: Dictionary containing Tile objects by their
            ID.
    """
    tiles: Dict[int, objects.Tile] = {}
    for tile_element in tile_element_list:
        # id is not optional
        id_ = int(tile_element.attrib["id"])

        # optional attributes
        _type = None
        try:
            _type = tile_element.attrib["type"]
        except KeyError:
            pass

        terrain = None
        try:
            tile_terrain_attrib = tile_element.attrib["terrain"]
        except KeyError:
            pass
        else:
            # below is an attempt to explain how terrains are handled.
            # 'terrain' attribute is a comma seperated list of 4 values,
            # each is either an integer or blank

            # convert to list of values
            terrain_list_attrib = re.split(",", tile_terrain_attrib)
            # terrain_list is list of indexes of Tileset.terrain_types
            terrain_list: List[Optional[int]] = []
            # each index in terrain_list_attrib refers to a corner
            for corner in terrain_list_attrib:
                if not corner:
                    terrain_list.append(None)
                else:
                    terrain_list.append(int(corner))
            terrain = objects.TileTerrain(*terrain_list)

        # tile element optional sub-elements
        properties: Optional[List[objects.Property]] = None
        tile_properties_element = tile_element.find("./properties")
        if tile_properties_element:
            properties = []
            property_list = tile_properties_element.findall("./property")
            for property_ in property_list:
                name = property_.attrib["name"]
                value = property_.attrib["value"]
                obj = objects.Property(name, value)
                properties.append(obj)

        # tile element optional sub-elements
        animation: Optional[List[objects.Frame]] = None
        tile_animation_element = tile_element.find("./animation")
        if tile_animation_element:
            animation = []
            frames = tile_animation_element.findall("./frame")
            for frame in frames:
                # tileid refers to the Tile.id of the animation frame
                animated_id = int(frame.attrib["tileid"])
                # duration is in MS. Should perhaps be converted to seconds.
                # FIXME: make decision
                duration = int(frame.attrib["duration"])
                animation.append(objects.Frame(animated_id, duration))

        # tile element optional sub-elements
        objectgroup: Optional[List[objects.TiledObject]] = None
        objectgroup_element = tile_element.find("./objectgroup")
        if objectgroup_element:
            objectgroup = []
            object_list = objectgroup_element.findall("./object")
            for object in object_list:
                my_id = object.attrib["id"]
                my_x = float(object.attrib["x"])
                my_y = float(object.attrib["y"])
                if "width" in object.attrib:
                    my_width = float(object.attrib["width"])
                else:
                    my_width = None
                if "height" in object.attrib:
                    my_height = float(object.attrib["height"])
                else:
                    my_height = None

                # This is where it would be nice if we could assume a walrus
                # operator was part of our Python distribution.

                my_object = None

                polygon = object.findall("./polygon")

                if polygon and len(polygon) > 0:
                    points = _parse_points(polygon[0].attrib["points"])
                    my_object = objects.PolygonObject(id_=my_id,
                                                      location=(my_x, my_y),
                                                      size=(my_width, my_height),
                                                      points=points)

                if my_object is None:
                    polyline  = object.findall("./polyline")

                    if polyline and len(polyline) > 0:
                        points = _parse_points(polyline[0].attrib["points"])
                        my_object = objects.PolylineObject(id_=my_id,
                                                           location=(my_x, my_y),
                                                           size=(my_width, my_height),
                                                           points=points)

                if my_object is None:
                    ellipse  = object.findall("./ellipse")

                    if ellipse and len(ellipse):
                        my_object = objects.ElipseObject(id_=my_id,
                                                         location=(my_x, my_y),
                                                         size=(my_width, my_height))


                if my_object is None:
                       my_object = objects.RectangleObject(id_=my_id,
                                                        location=(my_x, my_y),
                                                        size=(my_width, my_height))

                objectgroup.append(my_object)

        # if this is None, then the Tile is part of a spritesheet
        image = None
        image_element = tile_element.find("./image")
        if image_element is not None:
            image = _parse_image_element(image_element)

        # print(f"Adding '{id_}', {image}, {objectgroup}")

        tiles[id_] = objects.Tile(
            id_=id_,
            type_=_type,
            terrain=terrain,
            animation=animation,
            image=image,
            properties=properties,
            tileset=None,
            objectgroup=objectgroup
        )

    return tiles


def _parse_image_element(image_element: etree.Element) -> objects.Image:
    """Parse image element given.

    Args:
        image_element (etree.Element): Image element to be parsed.

    Returns:
        objects.Image: FIXME what is this?
    """
    # FIXME doc
    image = objects.Image(image_element.attrib["source"])

    width_attrib = image_element.attrib.get("width")
    height_attrib = image_element.attrib.get("height")

    if width_attrib and height_attrib:
        image.size = objects.Size(int(width_attrib), int(height_attrib))

    try:
        image.trans = image_element.attrib["trans"]
    except KeyError:
        pass

    return image


def _parse_properties_element(
    properties_element: etree.Element
) -> objects.Properties:
    """Adds Tiled property to Properties dict.

    Each property element has a number of attributes:
        name (str): Name of property.
        property_type (str): Type of property. Can be string, int, float,
            bool, color or file. Defaults to string.
        value (str): The value of the property.

    Args:
        properties_element (etree.Element): Element to be parsed.

    Returns:
        objects.Properties: Dict of the property values by property name.


    """
    properties: objects.Properties = {}
    for property_element in properties_element.findall("./property"):
        name = property_element.attrib["name"]
        try:
            property_type = property_element.attrib["type"]
        except KeyError:
            # strings do not have an attribute in property elements
            property_type = "string"
        value = property_element.attrib["value"]

        property_types = ["string", "int", "float", "bool", "color", "file"]
        assert (
            property_type in property_types
        ), f"Invalid type for property {name}"

        if property_type == "int":
            properties[name] = int(value)
        elif property_type == "float":
            properties[name] = float(value)
        elif property_type == "color":
            properties[name] = value
        elif property_type == "file":
            properties[name] = Path(value)
        elif property_type == "bool":
            if value == "true":
                properties[name] = True
            else:
                properties[name] = False
        else:
            properties[name] = value

    return properties


def _parse_tile_set(tile_set_element: etree.Element) -> objects.TileSet:
    """Parses a tile set that is embedded into a TMX.

    Args:
        tile_set_element (etree.Element): Element to be parsed.

    Returns:
        objects.TileSet: Tile Set from element.
    """
    # get all basic attributes
    name = tile_set_element.attrib["name"]
    max_tile_width = int(tile_set_element.attrib["tilewidth"])
    max_tile_height = int(tile_set_element.attrib["tileheight"])
    max_tile_size = objects.Size(max_tile_width, max_tile_height)

    spacing = None
    try:
        spacing = int(tile_set_element.attrib["spacing"])
    except KeyError:
        pass

    margin = None
    try:
        margin = int(tile_set_element.attrib["margin"])
    except KeyError:
        pass

    tile_count = None
    try:
        tile_count = int(tile_set_element.attrib["tilecount"])
    except KeyError:
        pass

    columns = None
    try:
        columns = int(tile_set_element.attrib["columns"])
    except KeyError:
        pass

    tile_offset = None
    tileoffset_element = tile_set_element.find("./tileoffset")
    if tileoffset_element is not None:
        tile_offset_x = int(tileoffset_element.attrib["x"])
        tile_offset_y = int(tileoffset_element.attrib["y"])
        tile_offset = objects.OrderedPair(tile_offset_x, tile_offset_y)

    grid = None
    grid_element = tile_set_element.find("./grid")
    if grid_element is not None:
        grid_orientation = grid_element.attrib["orientation"]
        grid_width = int(grid_element.attrib["width"])
        grid_height = int(grid_element.attrib["height"])
        grid = objects.Grid(grid_orientation, grid_width, grid_height)

    properties = None
    properties_element = tile_set_element.find("./properties")
    if properties_element is not None:
        properties = _parse_properties_element(properties_element)

    terrain_types: Optional[List[objects.Terrain]] = None
    terrain_types_element = tile_set_element.find("./terraintypes")
    if terrain_types_element is not None:
        terrain_types = []
        for terrain in terrain_types_element.findall("./terrain"):
            name = terrain.attrib["name"]
            terrain_tile = int(terrain.attrib["tile"])
            terrain_types.append(objects.Terrain(name, terrain_tile))

    image = None
    image_element = tile_set_element.find("./image")
    if image_element is not None:
        image = _parse_image_element(image_element)

    tile_element_list = tile_set_element.findall("./tile")
    tiles = _parse_tiles(tile_element_list)

    tileset = objects.TileSet(
        name,
        max_tile_size,
        spacing,
        margin,
        tile_count,
        columns,
        tile_offset,
        grid,
        properties,
        image,
        terrain_types,
        tiles,
    )

    # Go back and create a circular link so tiles know what tileset they are
    # part of. Needed for animation.
    for id_, tile in tiles.items():
        tile.tileset = tileset

    return tileset


def _get_tile_sets(
    map_element: etree.Element, parent_dir: Path
) -> objects.TileSetDict:
    """Get tile sets.

    Args:
        map_element (etree.Element): Element to be parsed.
        parent_dir (Path): Directory that TMX is in.

    Returns:
        objects.TileSetDict: Dict of tile sets in the TMX by first_gid
    """
    # parse all tilesets
    tile_sets: objects.TileSetDict = {}
    tile_set_element_list = map_element.findall("./tileset")
    for tile_set_element in tile_set_element_list:
        # tiled docs are ambiguous about the 'firstgid' attribute
        # current understanding is for the purposes of mapping the layer
        # data to the tile set data, add the 'firstgid' value to each
        # tile 'id'; this means that the 'firstgid' is specific to each,
        # tile set as they pertain to the map, not tile set specific as
        # the tiled docs can make it seem
        # 'firstgid' the key for each TileMap
        first_gid = int(tile_set_element.attrib["firstgid"])
        try:
            # check if is an external TSX
            source = tile_set_element.attrib["source"]
        except KeyError:
            # the tile set is embedded
            name = tile_set_element.attrib["name"]
            tile_sets[first_gid] = _parse_tile_set(tile_set_element)
        else:
            # tile set is external
            tile_sets[first_gid] = _parse_external_tile_set(
                parent_dir, tile_set_element
            )

    return tile_sets


def parse_tile_map(tmx_file: Union[str, Path]) -> objects.TileMap:
    """Parse tile map.

    Args:
        tmx_file (Union[str, Path]): TMX file to be parsed.

    Returns:
        objects.TileMap: TileMap object generated from the TMX file provided.
    """
    # setting up XML parsing
    map_tree = etree.parse(str(tmx_file))
    map_element = map_tree.getroot()

    # positional arguments for TileMap
    parent_dir = Path(tmx_file).parent

    version = map_element.attrib["version"]
    tiled_version = map_element.attrib["tiledversion"]
    orientation = map_element.attrib["orientation"]
    render_order = map_element.attrib["renderorder"]

    map_width = int(map_element.attrib["width"])
    map_height = int(map_element.attrib["height"])
    map_size = objects.Size(map_width, map_height)

    tile_width = int(map_element.attrib["tilewidth"])
    tile_height = int(map_element.attrib["tileheight"])
    tile_size = objects.Size(tile_width, tile_height)

    infinite_attribute = map_element.attrib["infinite"]
    infinite = bool(infinite_attribute == "true")

    if "nextlayerid" in map_element.attrib:
        next_layer_id = int(map_element.attrib["nextlayerid"])
    else:
        next_layer_id = None

    if "nextobjectid" in map_element.attrib:
        next_object_id = int(map_element.attrib["nextobjectid"])
    else:
        next_object_id = None

    tile_sets = _get_tile_sets(map_element, parent_dir)

    layers = _get_layers(map_element)

    tile_map = objects.TileMap(
        parent_dir,
        tmx_file,
        version,
        tiled_version,
        orientation,
        render_order,
        map_size,
        tile_size,
        infinite,
        next_layer_id,
        next_object_id,
        tile_sets,
        layers,
    )

    try:
        tile_map.hex_side_length = int(map_element.attrib["hexsidelength"])
    except KeyError:
        pass

    try:
        tile_map.stagger_axis = int(map_element.attrib["staggeraxis"])
    except KeyError:
        pass

    try:
        tile_map.stagger_index = int(map_element.attrib["staggerindex"])
    except KeyError:
        pass

    try:
        color = parse_color(map_element.attrib["backgroundcolor"])
        tile_map.background_color = (color.red, color.green, color.blue)
    except KeyError:
        pass

    properties_element = map_tree.find("./properties")
    if properties_element is not None:
        tile_map.properties = _parse_properties_element(properties_element)

    return tile_map
