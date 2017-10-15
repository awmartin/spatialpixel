import geojson


class SlippyLayer(object):
    def __init__(self, filename, strokeColor=None, fillColor=None, styler=None, keyer=None):
        self.filename = filename
        self.strokeColor = strokeColor if strokeColor is not None else color(255,0,0)
        self.fillColor = fillColor

        self.layerObject = geojson.RenderGeoJson.open(filename, styler, keyer)
        self.underlayMap = None

    def setUnderlayMap(self, m):
        self.underlayMap = m

    def render(self):
        self.layer = createGraphics(self.underlayMap.width, self.underlayMap.height)
        self.layer.beginDraw()

        if self.fillColor is not None:
            self.layer.fill(self.fillColor)
        else:
            self.layer.noFill()

        if self.strokeColor is not None:
            self.layer.stroke(self.strokeColor)
        else:
            self.layer.noStroke()

        self.layerObject.render(self.underlayMap.lonToX, self.underlayMap.latToY, self.layer)

        self.layer.endDraw()

    def draw(self):
        image(self.layer, 0, 0)
