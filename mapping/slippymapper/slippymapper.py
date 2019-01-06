import math
from ...util import lazyimages
from marker import *
from tile_servers import tile_servers
import sys

# TODO Extract the processing-specific code.

# Fundamental transformations. Reference: http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

def lonToTile(lon, zoom):
    """Given a longitude and zoom value, return the X map tile index."""
    n = 2.0 ** zoom
    return ((lon + 180.0) / 360.0) * n

def latToTile(lat, zoom):
    """Given a latitude and zoom value, return the Y map tile index."""
    n = 2.0 ** zoom
    lat_rad = math.radians(lat)
    return (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n

def tileToLon(tile, zoom):
    """Given a tile and zoom, give the longitude."""
    n = 2.0 ** zoom
    return tile / n * 360.0 - 180.0

def tileToLat(tile, zoom):
    """Given a tile and zoom, give the latitude."""
    n = 2.0 ** zoom
    lat_rad = math.atan(math.sinh(math.pi * (1.0 - 2.0 * tile / n)))
    return math.degrees(lat_rad)


class SlippyMapper(object):
    """SlippyMap will draw a map given a location, zoom, and public tile server."""

    tile_size = 256.0

    def __init__(self, lat, lon, zoom=12, server='toner', width=512, height=512):
        self._width = width
        self._height = height
        self._basemap = None

        self.set_server(server)

        self.lat = lat
        self.lon = lon
        self.set_zoom(zoom)

        self.centerX = lonToTile(self.lon, self.zoom)
        self.centerY = latToTile(self.lat, self.zoom)
        self.offsetX = floor((floor(self.centerX) - self.centerX) * self.tile_size)
        self.offsetY = floor((floor(self.centerY) - self.centerY) * self.tile_size)

        self.lazyImageManager = lazyimages.LazyImageManager()
        self.layers = []
        self.markers = []
    
    def set_server_url(self, zxyurl):
        """Allows you to set a custom Z/X/Y server URL instead of picking an included one.

        If you look at tile_servers.py, you'll see what these URLs typically look like.
        Currently, slippymapper assumes you're targeting a Z/X/Y server. For example:

            mymap.setServerUrl("https://tile.server.org/%s/%s/%s.png")
        
        The "%s" interpolation is automatically filled out with the Z, X, and Y values,
        respectively.
        """
        self.url = zxyurl
        self.server = 'custom'
    setServerUrl = set_server_url

    def set_server(self, server):
        """Set the current render server given the name of a predefined public server.

        See the tile_servers.py file for possible tile servers. All you need to do is provide
        the name of the server, like "carto-dark". This defaults to Stamen's "toner" server.

        Setting this after the map is rendered requires re-rendering the map by calling render().
        """
        if server in tile_servers:
            self.server = server
            self.url = tile_servers[server]
        
        elif server is None:
            # Don't render a map at all.
            self.server = None
            self.url = None
        
        else:
            sys.stderr.write("""Got %s as a tile server but that didn't exist. 
Available servers are %s. Falling back to 'toner'. 
You can also specify a custom ZXY URL with the setServerUrl() method.""" % \
                (server, ", ".join(tile_servers.keys())))
            self.server = 'toner'
            self.url = tile_servers['toner']
    setServer = set_server

    def set_zoom(self, zoom):
        self.zoom = max(min(zoom, 18), 0)
        self.centerX = lonToTile(self.lon, self.zoom)
        self.centerY = latToTile(self.lat, self.zoom)
    setZoom = set_zoom

    def set_center(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.centerX = lonToTile(self.lon, self.zoom)
        self.centerY = latToTile(self.lat, self.zoom)
    setCenter = set_center

    @property
    def has_rendered(self):
        return self._basemap is not None
    hasRendered = has_rendered

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
    
    @property
    def bounding_box(self):
        lonwest = self.xToLon(0)
        loneast = self.xToLon(self.width)
        latnorth = self.yToLat(0)
        latsouth = self.yToLat(self.height)
        return (latsouth, lonwest, latnorth, loneast)
    boundingBox = bounding_box
    bbox = bounding_box
    
    def set_size(self, width, height):
        self._width = width
        self._height = height

        # The basemap is None until we render the first time. So if it's not rendered, rebuild the map.
        # Thus, setting the size will require re-rendering the map.
        if self.has_rendered:
            self._basemap = createGraphics(floor(self._width), floor(self._height))
    setSize = set_size

    def clear(self):
        if self.has_rendered:
            self._basemap.beginDraw()
            self._basemap.background(255, 0)
            self._basemap.endDraw()
    
    @property
    def has_tile_server(self):
        return self.url is not None
    
    def get_tile_url(self, x, y):
        # Interpolate the URL for this particular tile.
        # e.g. .../12/1208/1541.png
        return self.url % (self.zoom, x, y)
    
    # Inspired by math contained in https://github.com/dfacts/staticmaplite/
    def render(self):
        """Create the map by requesting tiles from the specified tile server."""

        if not self.has_rendered:
            self._basemap = createGraphics(floor(self._width), floor(self._height))

        self.clear()

        if self.has_tile_server:
            numColumns = self.width / self.tile_size
            numRows = self.height / self.tile_size

            tiles_start_x = floor(self.centerX - numColumns / 2.0)
            tiles_start_y = floor(self.centerY - numRows / 2.0)

            tiles_end_x = ceil(self.centerX + numColumns / 2.0)
            tiles_end_y = ceil(self.centerY + numRows / 2.0)

            self.offsetX = -floor((self.centerX - floor(self.centerX)) * self.tile_size) + \
                floor(self.width / 2.0) + \
                floor(tiles_start_x - floor(self.centerX)) * self.tile_size
            self.offsetY = -floor((self.centerY - floor(self.centerY)) * self.tile_size) + \
                floor(self.height / 2.0) + \
                floor(tiles_start_y - floor(self.centerY)) * self.tile_size

            def onTileLoaded(tile, meta):
                self._basemap.beginDraw()
                x = meta['destX']
                y = meta['destY']
                self._basemap.image(tile, x, y)
                self._basemap.endDraw()

            for x in xrange(tiles_start_x, tiles_end_x):
                for y in xrange(tiles_start_y, tiles_end_y):
                    tile_url = self.get_tile_url(x, y)

                    # Compute the x and y coordinates for where this tile will go on the map.
                    destX = (x - tiles_start_x) * self.tile_size + self.offsetX
                    destY = (y - tiles_start_y) * self.tile_size + self.offsetY

                    # Attempts to load all the images lazily.
                    meta = {
                        'url' : tile_url,
                        'destX' : destX,
                        'destY' : destY,
                        'x' : x,
                        'y' : y,
                        }
                    self.lazyImageManager.addLazyImage(tile_url, onTileLoaded, meta)

        # Kick off all the layer rendering.
        for layer in self.layers:
            layer.render()

        for marker in self.markers:
            marker.draw()

    # TODO Revisit map filters.
    # def makeGrayscale(self):
    #     self._basemap.loadPixels()

    #     for i in xrange(0, self._basemap.width * self._basemap.height):
    #         b = self._basemap.brightness(self._basemap.pixels[i])
    #         self._basemap.pixels[i] = self._basemap.color(b, b, b)

    #     self._basemap.updatePixels()

    # def makeFaded(self):
    #     self._basemap.noStroke()
    #     self._basemap.fill(255, 255, 255, 128)
    #     self._basemap.rect(0, 0, width, height)

    def draw(self):
        """Draws the base map on the Processing sketch canvas."""

        self.updateLazyImageLoading()

        if self.has_tile_server and self.has_rendered:
            image(self._basemap, 0, 0)

        for layer in self.layers:
            layer.draw()

        for marker in self.markers:
            marker.draw()

    def updateLazyImageLoading(self):
        if self.lazyImageManager.allLazyImagesLoaded:
            return
        self.lazyImageManager.request()

    def add_marker(self, latitude, longitude, marker=None):
        if marker is None:
            m = CircleMarker(6)

        elif callable(marker):
            # The case that marker is a function of: x, y, pgraphics.
            m = SimpleMarker(marker)

        elif isinstance(marker, str):
            m = TextMarker(marker)

        elif isinstance(marker, unicode):
            m = TextMarker(str(marker))

        elif isinstance(marker, int) or isinstance(marker, float):
            m = CircleMarker(marker)

        elif isinstance(marker, PImage):
            m = ImageMarker(marker)

        else:
            m = marker

        m.setUnderlayMap(self)
        m.setLocation(latitude, longitude)

        self.markers.append(m)
        return m
    addMarker = add_marker

    def add_layer(self, layer):
        self.layers.append(layer)
        layer.setUnderlayMap(self)
    addLayer = add_layer

    def save(self, filename):
        self.flattened().save(filename)

    def flattened(self):
        export = createGraphics(self.width, self.height)
        export.beginDraw()

        if self.has_rendered and self.has_tile_server:
            export.image(self._basemap, 0, 0)

        for layer in self.layers:
            export.image(layer.layer, 0, 0)

        for marker in self.markers:
            marker.render(export)

        export.endDraw()
        return export

    def lonToX(self, lon):
        return (self.width / 2.0) - self.tile_size * (self.centerX - lonToTile(lon, self.zoom))

    def latToY(self, lat):
        return (self.height / 2.0) - self.tile_size * (self.centerY - latToTile(lat, self.zoom))

    def xToLon(self, x):
        tile = (x - (self.width / 2.0)) / self.tile_size + self.centerX
        return tileToLon(tile, self.zoom)

    def yToLat(self, y):
        tile = (y - (self.height / 2.0)) / self.tile_size + self.centerY
        return tileToLat(tile, self.zoom)

    def latlonToPixel(self, loc):
        return (self.lonToX(loc[0]), self.latToY(loc[1]))

    def pixelToLatLon(self, pixel):
        return (self.yToLat(pixel[1]), self.xToLon(pixel[0]))
