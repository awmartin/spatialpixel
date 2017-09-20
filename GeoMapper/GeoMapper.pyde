import geomap
import panner

import renderkml
import rendergeojson
import googledirections


def setup():
    size(1000, 800, P2D)

    # Create a new map, centered at Lower Manhattan, but twice the size of the sketch window.
    global geo
    geo = geomap.GeoMap(40.714728, -73.998672, 13, width*2, height*2, 'carto-dark')
    
    # Add some layers to the map. Don't add too many of these.
    # geo.addLayer(rendergeojson.Layer("route1762551746.geojson"))
    geo.addLayer(renderkml.Layer("location-history.kml"))
    
    googleApiKey = ''
    home = (40.748105,-73.955767)
    work = (40.740321,-73.993890)
    # geo.addLayer(googledirections.Layer(googleApiKey, home, work, mode='bicycling'))

    # Create a panner to provide a convenient panning interaction.
    # Offset the view half the dimensions of the sketch window, since we've made the map
    # twice the size of the sketch window.
    global pan
    pan = panner.Panner(this, x=-width/2, y=-height/2)

    # Actually render the map. Since this is expensive, we want to be explicit about when we render.
    geo.render()

    # lat, lon coordinates of some test markers.
    redColor = color(255,0,0)
    markers = [
        (40.714728, -73.998672, "Center", redColor),
        (40.689220, -74.044359, "Statue of Liberty", redColor),
        (40.808287, -73.960808, "Avery GSAPP", redColor),
        (40.792039, -73.886967, "Rikers Island", redColor),
        (40.748401, -73.985801, "Empire State Building", redColor),
        (40.660212, -73.968962, "Prospect Park", redColor),
        ]
    for marker in markers:
        geo.addMarker(marker)


def draw():
    background(255)

    pushMatrix()
    pan.pan()
    geo.draw()
    popMatrix()

    drawCoordinates()


def mouseDragged():
    pan.drag()

def keyPressed():
    lat = geo.yToLat(height / 2 - pan.panY)
    lon = geo.xToLon(width / 2 - pan.panX)

    if key in ("=", "+"):
        geo.setCenter(lat, lon)
        geo.setZoom(geo.zoom + 1)
        pan.reset()
        geo.render()
    elif key in ("-", "_"):
        geo.setCenter(lat, lon)
        geo.setZoom(geo.zoom - 1)
        pan.reset()
        geo.render()
    elif key in ("r", " "):
        geo.setCenter(lat, lon)
        pan.reset()
        geo.render()

def drawCoordinates():
    fill(255)
    noStroke()

    lat = geo.yToLat(mouseY - pan.panY)
    lon = geo.xToLon(mouseX - pan.panX)

    text(str(lat) + " x " + str(lon), 15, 25)
