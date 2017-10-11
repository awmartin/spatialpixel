import googledirections


class RenderableRoute(object):
    def __init__(self, route, strokeColor):
        self.route = route
        self.strokeColor = strokeColor

    def render(self, *args, **kwds):
        self.route.render(*args, **kwds)


class SlippyLayer(object):
    def __init__(self, apiKey, startLocation=None, endLocation=None, mode=None, strokeColor=None):
        self.apiKey = apiKey

        self.routes = []
        self.underlayMap = None

        # Backwards compatibility. *Deprecated*
        if startLocation is not None and endLocation is not None:
            self.addRoute(startLocation, endLocation, mode=mode, strokeColor=strokeColor)

    def setUnderlayMap(self, m):
        self.underlayMap = m

    def addRoute(self, start, end, mode='driving', strokeColor=color(0)):
        route = googledirections.RenderGoogleDirections(self.apiKey)
        # TODO Send directions requests asynchronously, or at least on first render, or request() method.
        route.request(start, end, mode)
        self.routes.append(RenderableRoute(route, strokeColor))

    def render(self):
        self.layer = createGraphics(self.underlayMap.width, self.underlayMap.height)
        self.layer.beginDraw()
        self.layer.noFill()

        for route in self.routes:
            self.layer.stroke(route.strokeColor)
            self.layer.strokeWeight(1.5)
            route.render(self.underlayMap.lonToX, self.underlayMap.latToY, self.layer)

        self.layer.endDraw()

    def draw(self):
        image(self.layer, 0, 0)
