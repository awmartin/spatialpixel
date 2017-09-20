import geomap
import panner
import samples


def setup():
    size(1000, 800, P2D)

    global geo
    # Create a new map, centered at Lower Manhattan, but twice the size of the sketch window.
    geo = geomap.GeoMap(40.714728, -73.998672, 13, width*2, height*2, 'carto-dark')

    # Create a panner to provide a convenient panning interaction.
    # Offset the view half the dimensions of the sketch window, since we've made the map
    # twice the size of the sketch window.
    global pan
    pan = panner.Panner(this, x=-width/2, y=-height/2)

    # Load some data we want to display over the map.
    samples.loadGeoJsonSample()
    # samples.loadKmlSample()
    samples.loadGoogleDirectionsSample()

    # Actually render the map. Since this is expensive, we want to be explicit about when we render.
    renderMap()

    # lat, lon coordinates of some test markers.
    global markers
    markers = [
        (40.714728, -73.998672, "Center"),
        (40.689220, -74.044359, "Statue of Liberty"),
        (40.808287, -73.960808, "Avery GSAPP"),
        (40.792039, -73.886967, "Rikers Island"),
        (40.748401, -73.985801, "Empire State Building"),
        (40.660212, -73.968962, "Prospect Park"),
        ]

def renderMap():
    """Render all the maps and samples."""
    
    global geo
    geo.renderBaseMap()
    
    samples.renderGeoJsonSample(geo)
    # samples.renderKmlSample(geo)
    samples.renderGoogleDirectionsSample(geo)


def draw():
    background(255)

    pushMatrix()

    pan.pan()
    geo.draw()
    
    samples.drawGeoJsonSample()
    # samples.drawKmlSample()
    samples.drawGoogleDirectionsSample()

    drawMarkers()
    
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
        renderMap()
    elif key in ("-", "_"):
        geo.setCenter(lat, lon)
        geo.setZoom(geo.zoom - 1)
        pan.reset()
        renderMap()
    elif key in ("r", " "):
        geo.setCenter(lat, lon)
        pan.reset()
        renderMap()

def drawCoordinates():
    fill(255)
    noStroke()

    lat = geo.yToLat(mouseY - pan.panY)
    lon = geo.xToLon(mouseX - pan.panX)

    text(str(lat) + " x " + str(lon), 15, 25)

def drawMarkers():
    # As long as there are only a few markers, this should work ok.
    fill(255, 0, 0)
    noStroke()
    for marker in markers:
        geo.drawMarker(*marker)
