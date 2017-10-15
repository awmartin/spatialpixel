import kml


def defaultkeyer(feature):
    return None

def defaultstyler(key, feature):
    feature.noFill()
    feature.stroke(255, 0, 0)

class SlippyLayer(object):
    def __init__(self, filename, styler=None, keyer=None):
        self.filename = filename
        self.styler = styler if styler is not None else defaultstyler
        self.keyer = keyer if keyer is not None else defaultkeyer

        self.layerObject = kml.RenderKML.open(filename, styler=self.styler, keyer=self.keyer)
        self.underlayMap = None

    def setUnderlayMap(self, m):
        self.underlayMap = m

    def render(self):
        self.layer = createGraphics(self.underlayMap.width, self.underlayMap.height)
        self.layer.beginDraw()
        self.layerObject.render(self.underlayMap.lonToX, self.underlayMap.latToY, self.layer)
        self.layer.endDraw()

    def draw(self):
        image(self.layer, 0, 0)
