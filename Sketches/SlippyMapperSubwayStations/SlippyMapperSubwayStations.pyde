import spatialpixel.mapping.slippymapper as slippymapper
import csv


def setup():
    size(1000, 800, P2D)

    global pin
    pin = loadImage("https://s3.amazonaws.com/spatialpixel/maps/map-pin-10px.png")

    global nyc
    nyc = slippymapper.SlippyMapper(40.714728, -73.898672, 11, 'carto-dark', width, height)

    with open('StationEntrances.csv') as f:
        reader = csv.reader(f)
        header = reader.next()

        for row in reader:
            latitude = float(row[3])
            longitude = float(row[4])

            # Simple marker examples, prepackaged in slippymapper.
            # nyc.addMarker(latitude, longitude)

            # You can even add a PImage directly.
            nyc.addMarker(latitude, longitude, pin)

            # Create a marker object so you can customize them.
            # circle = slippymapper.CircleMarker(5)
            # circle.stroke(255, 0, 0)
            # circle.noFill()
            # nyc.addMarker(latitude, longitude, circle)

            # TextMarker class (and other markers) can accept a color directly in its constructor.
            # nyc.addMarker(latitude, longitude, slippymapper.TextMarker(row[2], color(255)))

            # There's also a class for an X-shaped marker.
            # nyc.addMarker(latitude, longitude, slippymapper.CrossMarker(3))

            # Provide a function to draw an arbitrary marker.
            # nyc.addMarker(latitude, longitude, drawPin)

            # An interactive marker also drawn with a function.
            # nyc.addMarker(latitude, longitude, drawCross)

            # Custom interactive marker by subclassing DataMarker. Here, you can make a marker
            # by providing the data to the marker's constructor.
            # nyc.addMarker(latitude, longitude, StationMarker(row))

    nyc.render()

def draw():
    background(255)
    nyc.draw()


# Here are some marker drawing functions and classes used in some of the examples above.
# 'marker' is a PGraphics object.

def drawPin(x, y, marker):
    # The pin image we have places the pin's point at the bottom middle. So let's offset the
    # image to have x and y centered at the pin's bottom.
    marker.image(pin, x - pin.width / 2, y - pin.height)

def drawCross(x, y, marker):
    if dist(x, y, mouseX, mouseY) < 5:
        marker.stroke(255, 0, 0)
        marker.strokeWeight(4)
        marker.line(x - 3, y - 3, x + 3, y + 3)
        marker.line(x - 3, y + 3, x + 3, y - 3)
    else:
        marker.stroke(0, 255, 0)
        marker.strokeWeight(1)
        marker.line(x - 3, y - 3, x + 3, y + 3)
        marker.line(x - 3, y + 3, x + 3, y - 3)


class StationMarker(slippymapper.DataMarker):
    def drawMarker(self, x, y, marker):
        if dist(x, y, mouseX, mouseY) < 5 and mousePressed:
            marker.stroke(255, 0, 0)
            marker.strokeWeight(4)
            marker.line(x - 3, y - 3, x + 3, y + 3)
            marker.line(x - 3, y + 3, x + 3, y - 3)

            station_name = self.data[2]
            marker.text(station_name, x, y)
        else:
            marker.stroke(0, 255, 0)
            marker.strokeWeight(1)
            marker.line(x - 3, y - 3, x + 3, y + 3)
            marker.line(x - 3, y + 3, x + 3, y - 3)
