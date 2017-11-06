import geojson


def defaultstyler(data, feature):
    feature.noFill()
    feature.stroke(255, 0, 0)

class SlippyLayer(object):
    '''Creates a SlippyMapper layer for GeoJson objects.

    fileobj - instance of:
        str: contains a filename of the geojson file
        file: contains a file object for a geojson file
        RenderGeoJson: contains a RenderGeoJson instance
    '''
    def __init__(self, source, styler=None, drawfeatures=False):
        self.source = source
        if isinstance(source, geojson.RenderGeoJson):
            self.layerObject = source
        else:
            self.layerObject = geojson.RenderGeoJson(source)

        self.styler = styler if styler is not None else defaultstyler
        self.drawfeatures = drawfeatures

        self.underlayMap = None

    def setUnderlayMap(self, m):
        self.underlayMap = m

    def render(self):
        self.layer = createGraphics(self.underlayMap.width, self.underlayMap.height)
        self.layer.beginDraw()
        self.layerObject.render(self.underlayMap.lonToX, self.underlayMap.latToY, self.layer, self.styler)
        self.layer.endDraw()

    def draw(self):
        image(self.layer, 0, 0)
