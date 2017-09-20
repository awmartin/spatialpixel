import rendergeojson
import renderkml
import googledirections


# GeoJSON sample using running data exported from mapmyrun.com.

def loadGeoJsonSample():
    global geojsonpath
    with open("route1762551746.geojson") as f:
        geojsonpath = rendergeojson.RenderGeoJson(f)
    geojsonpath.parse()

def renderGeoJsonSample(geo):
    global geojsonimage
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

def renderKmlSample(geo):
    global kmlimage
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
    
    # Provide your Google API key here.
    apiKey = ''
    goodir = googledirections.GoogleDirections(apiKey)
    home = (40.748105,-73.955767)
    work = (40.740321,-73.993890)
    goodir.request(home, work, 'bicycling')

def renderGoogleDirectionsSample(geo):
    global goodirimg

    goodirimg = createGraphics(geo.w, geo.h)
    goodirimg.beginDraw()
    goodirimg.noFill()
    goodirimg.stroke(0, 255, 0)
    goodir.render(geo.lonToX, geo.latToY, goodirimg)
    goodirimg.endDraw()

def drawGoogleDirectionsSample():
    image(goodirimg, 0, 0)

