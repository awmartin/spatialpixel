import geomap
import rendergeojson
import renderkml
import googledirections
import panner


def setup():
    size(1000, 800, P2D)

    global geo
    # Create a new map, centered at Lower Manhattan, but twice the size of the sketch window.
    geo = geomap.GeoMap(40.714728, -73.998672, 13, width*2, height*2, 'carto-dark')

    # Apply some styling to the map in Processing if desired.
    # geo.makeGrayscale()
    # geo.makeFaded()

    # Create a panner to provide a convenient panning interaction.
    # Offset the view half the dimensions of the sketch window, since we've made the map
    # twice the size of the sketch window.
    global pan
    pan = panner.Panner(this, x=-width/2, y=-height/2)

    # Load some data we want to display over the map.
    loadGeoJsonSample()
    # loadKmlSample()
    loadGoogleDirectionsSample()

    # Actually render the map. Since this is expensive, we want to be explicit about when we render.
    geo.renderBaseMap()
    renderGeoJsonSample()
    # renderKmlSample()
    renderGoogleDirectionsSample()

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

def draw():
    background(255)

    pushMatrix()

    pan.pan()
    geo.draw()
    drawGeoJsonSample()
    # drawKmlSample()
    drawGoogleDirectionsSample()

    # As long as there are only a few markers, this should work ok.
    fill(255, 0, 0)
    noStroke()
    for marker in markers:
        geo.drawMarker(*marker)

    popMatrix()

    drawCoordinates()

def mouseDragged(self):
    pan.drag()

# def mouseWheel(event):
#     pan.zoom(event)

def keyPressed():
    if key == "+" or key == "=":
        geo.setZoom(geo.zoom + 1)
        renderMap()
    elif key == "-" or key == "_":
        geo.setZoom(geo.zoom - 1)
        renderMap()

def drawCoordinates():
    fill(255)
    noStroke()

    y = mouseY - pan.panY
    x = mouseX - pan.panX
    lat = geo.yToLat(y)
    lon = geo.xToLon(x)
    text(str(lat) + " x " + str(lon), 15, 25)


# -------------------------------------------------------------------------------------
# Samples


def renderMap():
    geo.renderBaseMap()
    # renderKmlSample()
    renderGeoJsonSample()
    renderGoogleDirectionsSample()


# GeoJSON sample using running data exported from mapmyrun.com.

def loadGeoJsonSample():
    global geojsonpath
    with open("route1762551746.geojson") as f:
        geojsonpath = rendergeojson.RenderGeoJson(f)
    geojsonpath.parse()

def renderGeoJsonSample():
    global geojsonimage, geo
    geojsonimage = createGraphics(geo.w, geo.h)

    geojsonimage.beginDraw()
    geojsonimage.noFill()
    geojsonimage.stroke(255, 0, 0)
    geojsonpath.render(geo.lonToX, geo.latToY, geojsonimage)
    geojsonimage.endDraw()

def drawGeoJsonSample():
    image(geojsonimage, 0, 0)


# KML sample using location history exported from Google as a KML file.

def loadKmlSample():
    global kmlpath
    with open("location-history.kml") as f:
        kmlpath = renderkml.RenderKML(f)
    kmlpath.parse()

def renderKmlSample():
    global kmlimage, geo
    kmlimage = createGraphics(geo.w, geo.h)

    kmlimage.beginDraw()
    kmlimage.noFill()
    kmlimage.stroke(255, 0, 0)
    kmlpath.render(geo.lonToX, geo.latToY, kmlimage)
    kmlimage.endDraw()

def drawKmlSample():
    image(kmlimage, 0, 0)


# Google Directions sample

def loadGoogleDirectionsSample():
    global goodir
    goodir = googledirections.GoogleDirections('')
    home = (40.748105,-73.955767)
    work = (40.740321,-73.993890)
    goodir.request(home, work, 'bicycling')

def renderGoogleDirectionsSample():
    global goodirimg, geo

    goodirimg = createGraphics(geo.w, geo.h)
    goodirimg.beginDraw()
    goodirimg.noFill()
    goodirimg.stroke(0, 255, 0)
    goodir.render(geo.lonToX, geo.latToY, goodirimg)
    goodirimg.endDraw()

def drawGoogleDirectionsSample():
    image(goodirimg, 0, 0)
