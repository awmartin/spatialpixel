import math
import lazyimages


def lonToTile(lon, zoom):
    """Given a longitude and zoom value, return the X map tile index."""
    n = 2.0 ** zoom
    return ((lon + 180.0) / 360.0) * n

def latToTile(lat, zoom):
    """Given a latitude and zoom value, return the Y map tile index."""
    n = 2.0 ** zoom
    return (1.0 - math.log(math.tan(lat * math.pi / 180.0) + 1.0 / math.cos(lat * math.pi / 180.0)) / math.pi) / 2.0 * n

def tileToLon(tile, zoom):
    """Given a tile and zoom, give the longitude."""
    n = 2.0 ** zoom
    return tile / n * 360.0 - 180.0

def tileToLat(tile, zoom):
    """Given a tile and zoom, give the latitude."""
    n = 2.0 ** zoom
    lat_rad = math.atan(math.sinh(math.pi * (1.0 - 2.0 * tile / n)))
    return math.degrees(lat_rad)



class GeoMap(object):
    """GeoMap will draw a map given a location, zoom, and public tile server."""
    
    # List of public map tile Z/X/Y map tile servers.
    tile_servers = {
        # http://maps.stamen.com/
        'toner'              : "http://tile.stamen.com/toner/%s/%s/%s.png",
        'toner-lines'        : "http://tile.stamen.com/toner-lines/%s/%s/%s.png",
        'toner-hybrid'       : "http://tile.stamen.com/toner-hybrid/%s/%s/%s.png",
        'toner-background'   : "http://tile.stamen.com/toner-background/%s/%s/%s.png",
        'toner-lite'         : "http://tile.stamen.com/toner-lite/%s/%s/%s.png",
        'terrain'            : "http://tile.stamen.com/terrain/%s/%s/%s.png",
        'terrain-lines'      : "http://tile.stamen.com/terrain-lines/%s/%s/%s.png",
        'terrain-background' : "http://tile.stamen.com/terrain-background/%s/%s/%s.png",
        'watercolor'         : "http://tile.stamen.com/watercolor/%s/%s/%s.png",
        
        # Found in https://github.com/dfacts/staticmaplite/blob/master/staticmap.php
        'mapnik'             : "http://tile.openstreetmap.org/%s/%s/%s.png",
        'cycle'              : "http://a.tile.opencyclemap.org/cycle/%s/%s/%s.png",
        
        # http://wiki.openstreetmap.org/wiki/Tile_servers
        'openstreetmap'      : "http://a.tile.openstreetmap.org/%s/%s/%s.png", # also http://b.* and https://c.*
        'wikimedia'          : "https://maps.wikimedia.org/osm-intl/%s/%s/%s.png",
        'carto-light'         : "http://a.basemaps.cartocdn.com/light_all/%s/%s/%s.png",
        'carto-dark'          : "http://a.basemaps.cartocdn.com/dark_all/%s/%s/%s.png",
        'openptmap'          : "http://www.openptmap.org/tiles/%s/%s/%s.png",
        'hikebike'           : "http://a.tiles.wmflabs.org/hikebike/%s/%s/%s.png",
        
        # https://carto.com/location-data-services/basemaps/
        # Note: These seem to be really slow.
        'carto-lightall'     : "http://cartodb-basemaps-1.global.ssl.fastly.net/light_all/%s/%s/%s.png",
        'carto-darkall'      : "http://cartodb-basemaps-1.global.ssl.fastly.net/dark_all/%s/%s/%s.png",
        'carto-lightnolabels': "http://cartodb-basemaps-1.global.ssl.fastly.net/light_nolabels/%s/%s/%s.png",
        'carto-darknolabels' : "http://cartodb-basemaps-1.global.ssl.fastly.net/dark_nolabels/%s/%s/%s.png",
        }
    
    tileSize = 256.0
    
    def __init__(self, lat, lon, zoom, w, h, server='toner'):
        self.baseMap = createGraphics(floor(w), floor(h))
        
        if server in self.tile_servers:
            self.url = self.tile_servers[server]
        else:
            print "Got %s as a tile server but that didn't exist. Available servers are %s. Falling back to 'toner'." % \
                (server, ", ".join(self.tile_servers.keys()))
            self.url = self.tile_servers['toner']
        
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
    
    def setZoom(self, zoom):
        print "Setting zoom to", zoom
        self.zoom = max(min(zoom, 18), 1)
        self.centerX = lonToTile(self.lon, self.zoom)
        self.centerY = latToTile(self.lat, self.zoom)
    
    def setCenter(self, lat, lon):
        print "Setting the center to", lat, lon
        self.lat = lat
        self.lon = lon
        self.centerX = lonToTile(self.lon, self.zoom)
        self.centerY = latToTile(self.lat, self.zoom)
    
    @property
    def w(self):
        return self.baseMap.width
    @property
    def h(self):
        return self.baseMap.height
    
    # Inspired by math contained in https://github.com/dfacts/staticmaplite/
    def render(self):
        """Create the map by requesting tiles from the specified tile server."""
        
        self.baseMap.beginDraw()
        self.baseMap.background(255)
        self.baseMap.endDraw()
        
        numColumns = self.w / self.tileSize
        numRows = self.h / self.tileSize
        
        startX = floor(self.centerX - numColumns / 2.0)
        startY = floor(self.centerY - numRows / 2.0)
        
        endX = ceil(self.centerX + numColumns / 2.0)
        endY = ceil(self.centerY + numRows / 2.0)
        
        self.offsetX = -floor((self.centerX - floor(self.centerX)) * self.tileSize) + \
            floor(self.w / 2.0) + \
            floor(startX - floor(self.centerX)) * self.tileSize
        self.offsetY = -floor((self.centerY - floor(self.centerY)) * self.tileSize) + \
            floor(self.h / 2.0) + \
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
            self.drawMarker(*marker)
    
    def updateLazyImageLoading(self):
        if self.lazyImageManager.allLazyImagesLoaded:
            return
        self.lazyImageManager.request()
    
    def drawMarker(self, markerLat, markerLon, *meta):
        """Draws a circular marker in the main Processing PGraphics space."""
        
        x = self.lonToX(markerLon)
        y = self.latToY(markerLat)
        
        if len(meta) >= 1:
            title = meta[0]
        else:
            title = None
        if len(meta) >= 2:
            fill(meta[1])
        else:
            fill(255)
        
        ellipse(x, y, 7, 7)
        if title is not None:
            text(title, x + 5, y - 5)
    
    def addLayer(self, layer):
        self.layers.append(layer)
        layer.setUnderlayMap(self)
    
    def addMarker(self, marker):
        self.markers.append(marker)
        
    def lonToX(self, lon):
        return (self.w / 2.0) - self.tileSize * (self.centerX - lonToTile(lon, self.zoom))
    
    def latToY(self, lat):
        return (self.h / 2.0) - self.tileSize * (self.centerY - latToTile(lat, self.zoom))

    def xToLon(self, x):
        tile = (x - (self.w / 2.0)) / self.tileSize + self.centerX
        return tileToLon(tile, self.zoom)

    def yToLat(self, y):
        tile = (y - (self.h / 2.0)) / self.tileSize + self.centerY
        return tileToLat(tile, self.zoom)


