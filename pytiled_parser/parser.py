import functools
import re
import base64
import zlib

from pathlib import Path

from typing import *

import pytiled_parser.objects as objects
import pytiled_parser.utilities as utilities

import xml.etree.ElementTree as etree

def _decode_base64_data(data_text, compression, layer_width):
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
        if byte_count % 4 == 0:
            byte_count = 0
            int_count += 1
            tile_grid[row_count].append(int_value)
            int_value = 0
            if int_count % layer_width == 0:
                row_count += 1
                tile_grid.append([])

    tile_grid.pop()
    return tile_grid


def _decode_csv_layer(data_text):
    """
    Decodes csv encoded layer data.

    Credit:
    """
    tile_grid = []
    lines = data_text.split("\n")
    # remove erronious empty lists due to a newline being on both ends of text
    lines = lines[1:]
    lines = lines[:-1]
    for line in lines:
        line_list = line.split(",")
        while '' in line_list:
            line_list.remove('')
        line_list_int = [int(item) for item in line_list]
        tile_grid.append(line_list_int)

    return tile_grid


def _decode_data(element: etree.Element, layer_width: int, encoding: str,
                 compression: Optional[str]) -> List[List[int]]:
    """
    Decodes data or chunk data.

    Args:
        :element (Element): Element to have text decoded.
        :layer_width (int): Number of tiles per column in this layer. Used
            for determining when to cut off a row when decoding base64
            encoding layers.
        :encoding (str): Encoding format of the layer data.
        :compression (str): Compression format of the layer data.
    """
    # etree.Element.text comes with an appended and a prepended '\n'
    supported_encodings = ['base64', 'csv']
    if encoding not in supported_encodings:
        raise ValueError('{encoding} is not a valid encoding')

    supported_compression = [None, 'gzip', 'zlib']
    if compression is not None:
        if encoding != 'base64':
            raise ValueError('{encoding} does not support compression')
        if compression not in supported_compression:
            raise ValueError('{compression} is not a valid compression type')

    try:
        data_text = element.text  # type: ignore
    except AttributeError:
        raise AttributeError('{element} lacks layer data.')

    if encoding == 'csv':
        return _decode_csv_layer(data_text)

    return _decode_base64_data(data_text, compression, layer_width)


def _parse_data(element: etree.Element,
                layer_width: int) -> objects.LayerData:
    """
    Parses layer data.

    Will parse CSV, base64, gzip-base64, or zlip-base64 encoded data.

    Args:
        :element (Element): Data element to parse.
        :width (int): Layer width. Used for base64 decoding.

    Returns:
        :LayerData: Data object containing layer data or chunks of data.
    """
    encoding = element.attrib['encoding']
    compression = None
    try:
        compression = element.attrib['compression']
    except KeyError:
        pass

    chunk_elements = element.findall('./chunk')
    if chunk_elements:
        chunks: List[objects.Chunk] = []
        for chunk_element in chunk_elements:
            x = int(chunk_element.attrib['x'])
            y = int(chunk_element.attrib['y'])
            location = objects.OrderedPair(x, y)
            width = int(chunk_element.attrib['width'])
            height = int(chunk_element.attrib['height'])
            layer_data = _decode_data(chunk_element, layer_width, encoding,
                                      compression)
            chunks.append(objects.Chunk(location, width, height, layer_data))
        return chunks

    return _decode_data(element, layer_width, encoding, compression)


def _parse_layer(element: etree.Element,
                 layer_type: objects.LayerType) -> objects.Layer:
    """
    Parse layer element given.
    """
    width = int(element.attrib['width'])
    height = int(element.attrib['height'])
    size = objects.OrderedPair(width, height)
    data_element = element.find('./data')
    if data_element is not None:
        data: objects.LayerData = _parse_data(data_element, width)
    else:
        raise ValueError('{element} has no child data element.')

    return objects.Layer(size, data, **layer_type.__dict__)


def _parse_layer_type(layer_element: etree.Element) -> objects.LayerType:
    """
    Parse layer type element given.
    """
    id = int(layer_element.attrib['id'])

    name = layer_element.attrib['name']

    layer_type_object = objects.LayerType(id, name)

    try:
        offset_x = float(layer_element.attrib['offsetx'])
    except KeyError:
        offset_x = 0

    try:
        offset_y = float(layer_element.attrib['offsety'])
    except KeyError:
        offset_y = 0
    offset = objects.OrderedPair(offset_x, offset_y)

    try:
        layer_type_object.opacity = round(
            float(layer_element.attrib['opacity']) * 255)
    except KeyError:
        pass

    properties_element = layer_element.find('./properties')
    if properties_element is not None:
        layer_type_object.properties = _parse_properties_element(
            properties_element)

    if layer_element.tag == 'layer':
        return _parse_layer(layer_element, layer_type_object)
    elif layer_element.tag == 'objectgroup':
        return _parse_object_group(layer_element, layer_type_object)
    # else:
    #     return _parse_layer_group(layer_element, layer_type_object)


def _parse_object_group(element: etree.Element,
                        layer_type: objects.LayerType) -> objects.ObjectGroup:
    """
    Parse object group element given.
    """
    object_elements = element.findall('./object')
    tile_objects: List[objects.Object] = []

    for object_element in object_elements:
        id = int(object_element.attrib['id'])
        location_x = float(object_element.attrib['x'])
        location_y = float(object_element.attrib['y'])
        location = objects.OrderedPair(location_x, location_y)

        object = objects.Object(id, location)

        try:
            width = float(object_element.attrib['width'])
        except KeyError:
            width = 0

        try:
            height = float(object_element.attrib['height'])
        except KeyError:
            height = 0

        object.size = objects.OrderedPair(width, height)

        try:
            object.opacity = round(
                float(object_element.attrib['opacity']) * 255)
        except KeyError:
            pass

        try:
            object.rotation = int(object_element.attrib['rotation'])
        except KeyError:
            pass

        try:
            object.name = object_element.attrib['name']
        except KeyError:
            pass

        properties_element = object_element.find('./properties')
        if properties_element is not None:
            object.properties = _parse_properties_element(properties_element)

        tile_objects.append(object)

    object_group = objects.ObjectGroup(tile_objects, **layer_type.__dict__)
    try:
        color = utilities.parse_color(element.attrib['color'])
    except KeyError:
        pass

    try:
        draw_order = element.attrib['draworder']
    except KeyError:
        pass

    return object_group


@functools.lru_cache()
def _parse_external_tile_set(parent_dir: Path, tile_set_element: etree.Element
                            ) -> objects.TileSet:
    """
    Parses an external tile set.

    Caches the results to speed up subsequent instances.
    """
    source = Path(tile_set_element.attrib['source'])
    tile_set_tree = etree.parse(str(parent_dir / Path(source))).getroot()

    return _parse_tile_set(tile_set_tree)


def _parse_tiles(tile_element_list: List[etree.Element]
                ) -> Dict[int, objects.Tile]:
    tiles: Dict[int, objects.Tile] = {}
    for tile_element in tile_element_list:
        # id is not optional
        id = int(tile_element.attrib['id'])

        # optional attributes
        type = None
        try:
            type = tile_element.attrib['type']
        except KeyError:
            pass

        tile_terrain = None
        try:
            tile_terrain_attrib = tile_element.attrib['terrain']
        except KeyError:
            pass
        else:
            # an attempt to explain how terrains are handled is below.
            # 'terrain' attribute is a comma seperated list of 4 values,
            # each is either an integer or blank

            # convert to list of values
            terrain_list_attrib = re.split(',', tile_terrain_attrib)
            # terrain_list is list of indexes of Tileset.terrain_types
            terrain_list: List[Optional[int]] = []
            # each index in terrain_list_attrib reffers to a corner
            for corner in terrain_list_attrib:
                if corner == '':
                    terrain_list.append(None)
                else:
                    terrain_list.append(int(corner))
            tile_terrain = objects.TileTerrain(*terrain_list)

        # tile element optional sub-elements
        animation: Optional[List[objects.Frame]] = None
        tile_animation_element = tile_element.find('./animation')
        if tile_animation_element:
            animation = []
            frames = tile_animation_element.findall('./frame')
            for frame in frames:
                # tileid reffers to the Tile.id of the animation frame
                tile_id = int(frame.attrib['tileid'])
                # duration is in MS. Should perhaps be converted to seconds.
                # FIXME: make decision
                duration = int(frame.attrib['duration'])
                animation.append(objects.Frame(tile_id, duration))

        # if this is None, then the Tile is part of a spritesheet
        tile_image = None
        tile_image_element = tile_element.find('./image')
        if tile_image_element is not None:
            tile_image = _parse_image_element(tile_image_element)

        object_group = None
        tile_object_group_element = tile_element.find('./objectgroup')
        if tile_object_group_element:
            ### FIXME: why did they do this :(
            pass

        tiles[id] = objects.Tile(id, type, tile_terrain, animation,
                                 tile_image, object_group)

    return tiles


def _parse_image_element(image_element: etree.Element) -> objects.Image:
    """
    Parse image element given.

    Returns:
        :Color: Color in Arcade's preffered format.
    """
    source = image_element.attrib['source']

    trans = None
    try:
        trans = utilities.parse_color(image_element.attrib['trans'])
    except KeyError:
        pass

    width = int(image_element.attrib['width'])
    height = int(image_element.attrib['height'])
    size = objects.OrderedPair(width, height)

    return objects.Image(source, size, trans)


def _parse_properties_element(properties_element: etree.Element
                             ) -> objects.Properties:
    """
    Adds Tiled property to Properties dict.

    Args:
        :name (str): Name of property.
        :property_type (str): Type of property. Can be string, int, float,
            bool, color or file. Defaults to string.
        :value (str): The value of the property.

    Returns:
        :Properties: Properties Dict object.
    """
    properties: objects.Properties = {}
    for property_element in properties_element.findall('./property'):
        name = property_element.attrib['name']
        try:
            property_type = property_element.attrib['type']
        except KeyError:
            # strings do not have an attribute in property elements
            property_type = 'string'
        value = property_element.attrib['value']

        property_types = ['string', 'int', 'float', 'bool', 'color', 'file']
        assert property_type in property_types, (
            f"Invalid type for property {name}")

        if property_type == 'int':
            properties[name] = int(value)
        elif property_type == 'float':
            properties[name] = float(value)
        elif property_type == 'color':
            properties[name] = utilities.parse_color(value)
        elif property_type == 'file':
            properties[name] = Path(value)
        elif property_type == 'bool':
            if value == 'true':
                properties[name] = True
            else:
                properties[name] = False
        else:
            properties[name] = value

    return properties


def _parse_tile_set(tile_set_element: etree.Element) -> objects.TileSet:
    """
    Parses a tile set that is embedded into a TMX.
    """
    # get all basic attributes
    name = tile_set_element.attrib['name']
    max_tile_width = int(tile_set_element.attrib['tilewidth'])
    max_tile_height = int(tile_set_element.attrib['tileheight'])
    max_tile_size = objects.OrderedPair(max_tile_width, max_tile_height)

    spacing = None
    try:
        spacing = int(tile_set_element.attrib['spacing'])
    except KeyError:
        pass

    margin = None
    try:
        margin = int(tile_set_element.attrib['margin'])
    except KeyError:
        pass

    tile_count = None
    try:
        tile_count = int(tile_set_element.attrib['tilecount'])
    except KeyError:
        pass

    columns = None
    try:
        columns = int(tile_set_element.attrib['columns'])
    except KeyError:
        pass

    tile_offset = None
    tileoffset_element = tile_set_element.find('./tileoffset')
    if tileoffset_element is not None:
        tile_offset_x = int(tileoffset_element.attrib['x'])
        tile_offset_y = int(tileoffset_element.attrib['y'])
        tile_offset = objects.OrderedPair(tile_offset_x, tile_offset_y)

    grid = None
    grid_element = tile_set_element.find('./grid')
    if grid_element is not None:
        grid_orientation = grid_element.attrib['orientation']
        grid_width = int(grid_element.attrib['width'])
        grid_height = int(grid_element.attrib['height'])
        grid = objects.Grid(grid_orientation, grid_width, grid_height)

    properties = None
    properties_element = tile_set_element.find('./properties')
    if properties_element is not None:
        properties = _parse_properties_element(properties_element)

    terrain_types: Optional[List[objects.Terrain]] = None
    terrain_types_element = tile_set_element.find('./terraintypes')
    if terrain_types_element is not None:
        terrain_types = []
        for terrain in terrain_types_element.findall('./terrain'):
            name = terrain.attrib['name']
            terrain_tile = int(terrain.attrib['tile'])
            terrain_types.append(objects.Terrain(name, terrain_tile))

    image = None
    image_element = tile_set_element.find('./image')
    if image_element is not None:
        image = _parse_image_element(image_element)

    tile_element_list = tile_set_element.findall('./tile')
    tiles = _parse_tiles(tile_element_list)

    return objects.TileSet(name, max_tile_size, spacing, margin, tile_count,
                           columns, tile_offset, grid, properties, image,
                           terrain_types, tiles)


def parse_tile_map(tmx_file: Union[str, Path]):
    # setting up XML parsing
    map_tree = etree.parse(str(tmx_file))
    map_element = map_tree.getroot()

    # positional arguments for TileMap
    parent_dir = Path(tmx_file).parent

    version = map_element.attrib['version']
    tiled_version = map_element.attrib['tiledversion']
    orientation = map_element.attrib['orientation']
    render_order = map_element.attrib['renderorder']
    map_width = int(map_element.attrib['width'])
    map_height = int(map_element.attrib['height'])
    map_size = objects.OrderedPair(map_width, map_height)
    tile_width = int(map_element.attrib['tilewidth'])
    tile_height = int(map_element.attrib['tileheight'])
    tile_size = objects.OrderedPair(tile_width, tile_height)

    infinite_attribute = map_element.attrib['infinite']
    infinite = True if infinite_attribute == 'true' else False

    next_layer_id = int(map_element.attrib['nextlayerid'])
    next_object_id = int(map_element.attrib['nextobjectid'])

    # parse all tilesets
    tile_sets: Dict[int, objects.TileSet] = {}
    tile_set_element_list = map_element.findall('./tileset')
    for tile_set_element in tile_set_element_list:
        # tiled docs are ambiguous about the 'firstgid' attribute
        # current understanding is for the purposes of mapping the layer
        # data to the tile set data, add the 'firstgid' value to each
        # tile 'id'; this means that the 'firstgid' is specific to each,
        # tile set as they pertain to the map, not tile set specific as
        # the tiled docs can make it seem
        # 'firstgid' is saved beside each TileMap
        firstgid = int(tile_set_element.attrib['firstgid'])
        try:
            # check if is an external TSX
            source = tile_set_element.attrib['source']
        except KeyError:
            # the tile set in embedded
            name = tile_set_element.attrib['name']
            tile_sets[firstgid] = _parse_tile_set(tile_set_element)
        else:
            # tile set is external
            tile_sets[firstgid] = _parse_external_tile_set(
                parent_dir, tile_set_element)

    # parse all layers
    layers: List[objects.LayerType] = []
    layer_tags = ['layer', 'objectgroup', 'group']
    for element in map_element.findall('./'):
        if element.tag not in layer_tags:
            # only layer_tags are layer elements
            continue
        layers.append(_parse_layer_type(element))

    tile_map = objects.TileMap(parent_dir, version, tiled_version,
                               orientation, render_order, map_size, tile_size,
                               infinite, next_layer_id, next_object_id,
                               tile_sets, layers)

    try:
        tile_map.hex_side_length = int(map_element.attrib['hexsidelength'])
    except KeyError:
        pass

    try:
        tile_map.stagger_axis = int(map_element.attrib['staggeraxis'])
    except KeyError:
        pass

    try:
        tile_map.stagger_index = int(map_element.attrib['staggerindex'])
    except KeyError:
        pass

    try:
        backgroundcolor = map_element.attrib['backgroundcolor']
    except KeyError:
        pass
    else:
        tile_map.background_color = utilities.parse_color(backgroundcolor)

    properties_element = map_tree.find('./properties')
    if properties_element is not None:
        tile_map.properties = _parse_properties_element(properties_element)

    return tile_map
