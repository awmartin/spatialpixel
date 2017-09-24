import googledirections

class SlippyLayer(object):
    def __init__(self, apiKey, startLocation, endLocation, mode='driving', strokeColor=color(255,0,0), fillColor=None):
        self.apiKey = apiKey
        self.startLocation = startLocation
        self.endLocation = endLocation
        self.mode = mode
        self.strokeColor = strokeColor
        self.fillColor = fillColor

        self.layerObject = googledirections.RenderGoogleDirections(apiKey)
        self.underlayMap = None

        self.layerObject.request(self.startLocation, self.endLocation, self.mode)

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

        self.layer.strokeWeight(1.5)

        self.layerObject.render(self.underlayMap.lonToX, self.underlayMap.latToY, self.layer)

        self.layer.endDraw()

    def draw(self):
        image(self.layer, 0, 0)
