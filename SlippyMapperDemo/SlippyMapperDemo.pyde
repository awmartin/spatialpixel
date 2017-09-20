import slippymapper
import panner

import renderkml
import rendergeojson
import googledirections


def setup():
    size(1000, 800, P2D)

    # Create a new map, centered at Lower Manhattan, but twice the size of the sketch window.
    global slippy
    slippy = slippymapper.SlippyMapper(40.714728, -73.998672, 13, width*2, height*2, 'carto-dark')
    
    # Add some layers to the map. Don't add too many of these.
    slippy.addLayer(rendergeojson.Layer("route1762551746.geojson"))
    # slippy.addLayer(renderkml.Layer("location-history.kml"))
    
    googleApiKey = ''
    home = (40.748105, -73.955767)
    work = (40.740321, -73.993890)
    slippy.addLayer(googledirections.Layer(googleApiKey, home, work, mode='bicycling'))

    # Create a panner to provide a convenient panning interaction.
    # Offset the view half the dimensions of the sketch window, since we've made the map
    # twice the size of the sketch window.
    global pan
    pan = panner.Panner(this, x=-width/2, y=-height/2)

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
        slippy.addMarker(marker)
    
    # Actually render the map. Since this is expensive, we want to be explicit about when we render.
    slippy.render()


def draw():
    background(255)

    pushMatrix()
    pan.pan()
    slippy.draw()
    popMatrix()

    drawGui()


# --------------------------------------------------------------------------------------
# Interaction

def mouseDragged():
    pan.drag()

def keyPressed():
    lat = slippy.yToLat(height / 2 - pan.panY)
    lon = slippy.xToLon(width / 2 - pan.panX)

    if key in ("=", "+"):   # Zoom in
        slippy.setCenter(lat, lon)
        slippy.setZoom(slippy.zoom + 1)
        pan.reset()
        slippy.render()
    elif key in ("-", "_"):   # Zoom out
        slippy.setCenter(lat, lon)
        slippy.setZoom(slippy.zoom - 1)
        pan.reset()
        slippy.render()
    elif key in ("r", " "):    # Recenter the map
        slippy.setCenter(lat, lon)
        pan.reset()
        slippy.render()


# --------------------------------------------------------------------------------------
# GUI

def drawGui():
    drawCoordinates()
    drawHelp()

def drawCoordinates():
    fill(255)
    noStroke()

    lat = slippy.yToLat(mouseY - pan.panY)
    lon = slippy.xToLon(mouseX - pan.panX)

    text(str(lat) + " x " + str(lon), 15, 25)

def drawHelp():
    fill(255)
    noStroke()
    text("+/- zoom, spacebar to recenter", 15, 40)

