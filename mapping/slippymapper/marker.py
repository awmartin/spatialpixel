
class SlippyMarker(object):
    def __init__(self, markerLat, markerLon, markerColor=None, markerTitle=None):
        self.markerLat = markerLat
        self.markerLon = markerLon
        self.markerColor = markerColor
        self.markerTitle = markerTitle

    def setUnderlayMap(self, m):
        self.underlayMap = m

    def render(self, pgraphics):
        x = self.underlayMap.lonToX(self.markerLon)
        y = self.underlayMap.latToY(self.markerLat)

        if self.markerColor is not None:
            pgraphics.fill(self.markerColor)
        pgraphics.ellipse(x, y, 7, 7)
        if self.markerTitle is not None:
            pgraphics.text(self.markerTitle, x + 5, y - 5)

    def draw(self):
        x = self.underlayMap.lonToX(self.markerLon)
        y = self.underlayMap.latToY(self.markerLat)

        if self.markerColor is not None:
            fill(self.markerColor)
        ellipse(x, y, 7, 7)
        if self.markerTitle is not None:
            text(self.markerTitle, x + 5, y - 5)
