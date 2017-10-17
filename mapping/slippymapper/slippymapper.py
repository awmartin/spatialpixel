import math
from ...util import lazyimages
from marker import *
from tile_servers import tile_servers
import sys


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

    tileSize = 256.0

    def __init__(self, lat, lon, zoom, server='toner', width=512, height=512):
        self.baseMap = createGraphics(floor(width), floor(height))

        self.setServer(server)

        self.lat = lat
        self.lon = lon
        self.setZoom(zoom)

        self.centerX = lonToTile(self.lon, self.zoom)
        self.centerY = latToTile(self.lat, self.zoom)
        self.offsetX = floor((floor(self.centerX) - self.centerX) * self.tileSize)
        self.offsetY = floor((floor(self.centerY) - self.centerY) * self.tileSize)

        self.lazyImageManager = lazyimages.LazyImageManager()
        self.layers = []
        self.markers = []

    def setServer(self, server):
        self.server = server
        if server in tile_servers:
            self.url = tile_servers[server]
        else:
            sys.stderr.write("Got %s as a tile server but that didn't exist. Available servers are %s. Falling back to 'toner'." % \
                (server, ", ".join(tile_servers.keys())))
            self.url = tile_servers['toner']

    def setZoom(self, zoom):
        self.zoom = max(min(zoom, 18), 0)
        self.centerX = lonToTile(self.lon, self.zoom)
        self.centerY = latToTile(self.lat, self.zoom)

    def setCenter(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.centerX = lonToTile(self.lon, self.zoom)
        self.centerY = latToTile(self.lat, self.zoom)

    @property
    def width(self):
        return self.baseMap.width
    @property
    def height(self):
        return self.baseMap.height

    # Inspired by math contained in https://github.com/dfacts/staticmaplite/
    def render(self):
        """Create the map by requesting tiles from the specified tile server."""

        self.baseMap.beginDraw()
        self.baseMap.background(255)
        self.baseMap.endDraw()

        numColumns = self.width / self.tileSize
        numRows = self.height / self.tileSize

        startX = floor(self.centerX - numColumns / 2.0)
        startY = floor(self.centerY - numRows / 2.0)

        endX = ceil(self.centerX + numColumns / 2.0)
        endY = ceil(self.centerY + numRows / 2.0)

        self.offsetX = -floor((self.centerX - floor(self.centerX)) * self.tileSize) + \
            floor(self.width / 2.0) + \
            floor(startX - floor(self.centerX)) * self.tileSize
        self.offsetY = -floor((self.centerY - floor(self.centerY)) * self.tileSize) + \
            floor(self.height / 2.0) + \
            floor(startY - floor(self.centerY)) * self.tileSize

        def onTileLoaded(tile, meta):
            self.baseMap.beginDraw()
            x = meta['destX']
            y = meta['destY']
            self.baseMap.image(tile, x, y)
            self.baseMap.endDraw()

        for x in xrange(startX, endX):
            for y in xrange(startY, endY):
                # Interpolate the URL for this particular tile.
                # 12/1208/1541.png
                url = self.url % (self.zoom, x, y)

                # Compute the x and y coordinates for where this tile will go on the map.
                destX = (x - startX) * self.tileSize + self.offsetX
                destY = (y - startY) * self.tileSize + self.offsetY

                # Attempts to load all the images lazily.
                meta = {
                    'url' : url,
                    'destX' : destX,
                    'destY' : destY,
                    'x' : x,
                    'y' : y,
                    }
                self.lazyImageManager.addLazyImage(url, onTileLoaded, meta)

        # Kick off all the layer rendering.
        for layer in self.layers:
            layer.render()

        for marker in self.markers:
            marker.draw()

    # TODO Revisit map filters.
    # def makeGrayscale(self):
    #     self.baseMap.loadPixels()

    #     for i in xrange(0, self.baseMap.width * self.baseMap.height):
    #         b = self.baseMap.brightness(self.baseMap.pixels[i])
    #         self.baseMap.pixels[i] = self.baseMap.color(b, b, b)

    #     self.baseMap.updatePixels()

    # def makeFaded(self):
    #     self.baseMap.noStroke()
    #     self.baseMap.fill(255, 255, 255, 128)
    #     self.baseMap.rect(0, 0, width, height)

    def draw(self):
        """Draws the base map on the Processing sketch canvas."""

        self.updateLazyImageLoading()

        image(self.baseMap, 0, 0)

        for layer in self.layers:
            layer.draw()

        for marker in self.markers:
            marker.draw()

    def updateLazyImageLoading(self):
        if self.lazyImageManager.allLazyImagesLoaded:
            return
        self.lazyImageManager.request()

    def addMarker(self, latitude, longitude, marker=None):
        if marker is None:
            m = CircleMarker(6)

        elif callable(marker):
            # The case that marker is a function of: x, y, pgraphics.
            m = SimpleMarker(marker)

        elif isinstance(marker, str):
            m = TextMarker(marker)

        elif isinstance(marker, int) or isinstance(marker, float):
            m = CircleMarker(marker)

        elif isinstance(marker, PImage):
            m = ImageMarker(marker)

        else:
            m = marker

        m.setUnderlayMap(self)
        m.setLocation(latitude, longitude)

        self.markers.append(m)

    def addLayer(self, layer):
        self.layers.append(layer)
        layer.setUnderlayMap(self)

    def save(self, filename):
        self.flattened().save(filename)

    def flattened(self):
        export = createGraphics(self.width, self.height)
        export.beginDraw()

        export.image(self.baseMap, 0, 0)

        for layer in self.layers:
            export.image(layer.layer, 0, 0)

        for marker in self.markers:
            marker.render(export)

        export.endDraw()
        return export

    def lonToX(self, lon):
        return (self.width / 2.0) - self.tileSize * (self.centerX - lonToTile(lon, self.zoom))

    def latToY(self, lat):
        return (self.height / 2.0) - self.tileSize * (self.centerY - latToTile(lat, self.zoom))

    def xToLon(self, x):
        tile = (x - (self.width / 2.0)) / self.tileSize + self.centerX
        return tileToLon(tile, self.zoom)

    def yToLat(self, y):
        tile = (y - (self.height / 2.0)) / self.tileSize + self.centerY
        return tileToLat(tile, self.zoom)

    def latlonToPixel(self, loc):
        return (self.lonToX(loc[0]), self.latToY(loc[1]))

    def pixelToLatLon(self, pixel):
        return (self.yToLat(pixel[1]), self.xToLon(pixel[0]))
