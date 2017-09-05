import geomap
import rendergeojson
import renderkml


def setup():
    size(1000, 800, P2D)
    noLoop()

def draw():
    background(255)
    
    # Create a new map, centered at Lower Manhattan, filling the size of the sketch.
    geo = geomap.GeoMap(40.714728, -73.998672, 13, width, height, 'terrain')
    geo.createBaseMap()
    
    # Apply some styling to the map in Processing.
    geo.makeGrayscale()
    # geo.makeFaded()
    
    geo.draw()
    
    # lat, lon coordinates of some test markers.
    markers = [
        (40.714728, -73.998672, "Center"),
        (40.689220, -74.044359, "Statue of Liberty"),
        (40.808287, -73.960808, "Avery GSAPP"),
        (40.792039, -73.886967, "Rikers Island"),
        (40.748401, -73.985801, "Empire State Building"),
        (40.660212, -73.968962, "Prospect Park"),
        ]

    fill(255, 0, 0)
    noStroke()
    for marker in markers:
        geo.drawMarker(*marker)
    
    noFill()
    stroke(255, 0, 0)
    # with open("route1762551746.geojson") as f:
    #     path = rendergeojson.RenderGeoJson(f)
    # path.draw(geo.lonToX, geo.latToY)

    with open("route1762551746.kml") as f:
        kml = renderkml.RenderKML(f)
    kml.parse()
    kml.draw(geo.lonToX, geo.latToY)

    