import slippymapper
import panner

import renderkml
import rendergeojson
import googledirections

import csv

def setup():
    size(1000, 800, P2D)


    # Create a new map, centered at Lower Manhattan, at zoom level 12.
    # Make it twice the size of the sketch window.
    global slippy
    slippy = slippymapper.SlippyMapper(40.714728, -73.998672, 12, width*2, height*2, 'carto-light')
    
    # Adding a single marker.
    slippy.addMarker(40.808238, -73.959277, color(255,0,0), "Avery GSAPP")
    
    slippy.addLayer(rendergeojson.SlippyLayer("route1762551746.geojson"))
    # slippy.addLayer(renderkml.SlippyLayer("location-history.kml"))
    
    
    # Render all the different ways you can get from point a to b.
    apiKey = ''
    a = (40.808238, -73.959277)
    b = (40.748105, -73.955767)
    slippy.addLayer(googledirections.SlippyLayer(apiKey, a, b, mode='bicycling', strokeColor=color(0,255,0)))
    # slippy.addLayer(googledirections.SlippyLayer(apiKey, a, b, mode='walking', strokeColor=color(0,0,255)))
    # slippy.addLayer(googledirections.SlippyLayer(apiKey, a, b, mode='driving', strokeColor=color(255,0,0)))
    # slippy.addLayer(googledirections.SlippyLayer(apiKey, a, b, mode='transit', strokeColor=color(0,255,255)))
    
    
    # Speculate on routes taken by actual Citibike customers.
    with open('citibike.csv') as f:
        reader = csv.reader(f)
        header = reader.next()
        for row in reader:
            start_lat = float(row[5])
            start_lon = float(row[6])
            a = (start_lat, start_lon)
            
            end_lat = float(row[9])
            end_lon = float(row[10])
            b = (end_lat, end_lon)
            
            route = googledirections.SlippyLayer(apiKey, a, b, mode='bicycling', strokeColor=color(0,255,0))
            slippy.addLayer(route)
    
    
    # Render the map. Since this is expensive, we should be explicit about when this happens.
    slippy.render()


    # Create a panner to provide a convenient panning interaction.
    # Offset the map such that the center of the slippy map shows up in the center of the sketch.
    global pan
    pan = panner.Panner(this, x=-(slippy.width - width)/2, y=-(slippy.height - height)/2)


def draw():
    background(255)

    pushMatrix()
    pan.pan()
    slippy.draw()
    
    # Draw something in the space of the map.
    stroke(255,0,0)
    noFill()
    
    jfk_y = slippy.latToY(40.6413)
    jfk_x = slippy.lonToX(-73.7781)
    ellipse(jfk_x, jfk_y, 50, 50)
    
    lga_y = slippy.latToY(40.7769)
    lga_x = slippy.lonToX(-73.8740)
    ellipse(lga_x, lga_y, 50, 50)
    
    line(lga_x, lga_y, jfk_x, jfk_y)
    
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
        
    elif key == 'e':
        print "Exporting the base map..."
        slippy.baseMap.save("output/basemap.png")
        print "Done exporting."


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