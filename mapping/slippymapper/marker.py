"""Defines classes used to draw markers on a SlippyMapper instance.

There are several ways to add a marker to a SlippyMapper, all use the addMarker()
method in the SlippyMapper class.

1. Provide a string or number:

    map.addMarker(40.71, -73.9, "New York City")
    map.addMarker(40.71, -73.9, 3)

In the latter, the marker is a circle by default.

2. Provide a function:

    def cross(x, y, marker):
        marker.ellipse(x, y, 4, 4)
    map.addMarker(latitude, longitude, cross)

With this, you can start marking the marker interactive.

3. Provide an instance of a prepackaged class, derived from SimpleMarker: TextMarker, CrossMarker, etc.

4. Provide an instance fo a custom class, derived from DataMarker. Use when you need to bind
data to a marker for more complex rendering.

"""

class SimpleMarker(object):
    def __init__(self, draw):
        self.drawMarker = draw # self, x, y, pgraphics

        self.latitude = None
        self.longitude = None
        self.underlayMap = None

        self.strokeColor = color(0)
        self.fillColor = color(255)

        self.offsetX = 0
        self.offsetY = 0

    def stroke(self, r=None, g=None, b=None, a=None):
        if g is None and b is None and a is None:
            self.strokeColor = color(r)
        elif b is None and a is None:
            self.strokeColor = color(r, g)
        elif a is None:
            self.strokeColor = color(r, g, b)
        else:
            self.strokeColor = color(r, g, b, a)

    def fill(self, r=None, g=None, b=None, a=None):
        if g is None and b is None and a is None:
            self.fillColor = color(r)
        elif b is None and a is None:
            self.fillColor = color(r, g)
        elif a is None:
            self.fillColor = color(r, g, b)
        else:
            self.fillColor = color(r, g, b, a)

    def noStroke(self):
        self.strokeColor = None

    def noFill(self):
        self.fillColor = None

    def setColors(self, pgraphics):
        if self.strokeColor is None:
            pgraphics.noStroke()
        else:
            pgraphics.stroke(self.strokeColor)

        if self.fillColor is None:
            pgraphics.noFill()
        else:
            pgraphics.fill(self.fillColor)

    def setLocation(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def setUnderlayMap(self, m):
        self.underlayMap = m

    def setOffset(self, dx, dy):
        self.offsetx = dx
        self.offsety = dy

    def render(self, pgraphics):
        x = self.underlayMap.lonToX(self.longitude) + self.offsetX
        y = self.underlayMap.latToY(self.latitude) + self.offsetY

        self.setColors(pgraphics)
        self.drawMarker(x, y, pgraphics)

    def draw(self):
        x = self.underlayMap.lonToX(self.longitude) + self.offsetX
        y = self.underlayMap.latToY(self.latitude) + self.offsetY

        self.setColors(this)
        self.drawMarker(x, y, this)


class CircleMarker(SimpleMarker):
    def __init__(self, diameter, color=None):
        self.diameter = diameter

        super(CircleMarker, self).__init__(self.drawCircle)

        if color is not None:
            self.stroke(color)
            self.fill(color)

    def drawCircle(self, x, y, pgraphics):
        pgraphics.ellipse(x, y, self.diameter, self.diameter)


class TextMarker(SimpleMarker):
    def __init__(self, text, color=None):
        self.text = text

        super(TextMarker, self).__init__(self.drawText)

        self.noStroke()
        if color is not None:
            self.fill(color)
        else:
            self.fill(0)

    def drawText(self, x, y, pgraphics):
        pgraphics.text(self.text, x, y)


class CrossMarker(SimpleMarker):
    def __init__(self, size, color=None):
        self.size = size

        super(CrossMarker, self).__init__(self.drawCross)

        if color is not None:
            self.stroke(color)
        self.noFill()

    def drawCross(self, x, y, pgraphics):
        pgraphics.line(x - self.size, y - self.size, x + self.size, y + self.size)
        pgraphics.line(x - self.size, y + self.size, x + self.size, y - self.size)

class ImageMarker(SimpleMarker):
    def __init__(self, image):
        self.image = image

        super(ImageMarker, self).__init__(self.drawImage)

        # Adjust for the center of the image by default.
        self.offsetX = - self.image.width / 2
        self.offsetY = - self.image.height / 2

    def drawImage(self, x, y, pgraphics):
        pgraphics.image(self.image, x, y)


class DataMarker(object):
    def __init__(self, data):
        self.data = data

        self.latitude = None
        self.longitude = None
        self.underlayMap = None

    def setLocation(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def setUnderlayMap(self, m):
        self.underlayMap = m

    def drawMarker(self, x, y, marker):
        pass

    def render(self, pgraphics):
        x = self.underlayMap.lonToX(self.longitude)
        y = self.underlayMap.latToY(self.latitude)

        self.drawMarker(x, y, pgraphics)

    def draw(self):
        self.render(this)
