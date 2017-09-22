import slippymapper
import panner

import renderkml
import rendergeojson
import googledirections

import csv

def setup():
    size(1000, 800, P2D)
    
    # Create a new slippy map, centered at Lower Manhattan, at zoom level 12.
    # Make it twice the size of the sketch window. Pick a renderer. For more renders, check slippymapper.py.
    global slippy
    slippy = slippymapper.SlippyMapper(40.714728, -73.998672, 12, width*2, height*2, 'carto-light')
    
    
    # Adding single markers.
    slippy.addMarker(40.808238, -73.959277, color(255,0,0), "Avery GSAPP")
    slippy.addMarker(40.689220, -74.044359, color(255,0,0), "Statue of Liberty")
    slippy.addMarker(40.660212, -73.968962, color(255,0,0), "Prospect Park")
    
    # An example running route from mapmyrun.com.
    slippy.addLayer(rendergeojson.SlippyLayer("route1762551746.geojson"))
    
    # To view the earthquakes sample, try setting the map zoom above to 3.
    # slippy.addLayer(rendergeojson.SlippyLayer("earthquakes_all_day_20170921.geojson"))
    
    # If you download your Location History from Google, you can export as KML and attempt to load it here.
    # It currently shows the locations it contains as points.
    # slippy.addLayer(renderkml.SlippyLayer("google-location-history.kml"))
    
    
    # Render all the different ways you can get from point a to b.
    apiKey = ''
    a = (40.808238, -73.959277)
    b = (40.745530, -73.946631)
    slippy.addLayer(googledirections.SlippyLayer(apiKey, a, b, mode='bicycling', strokeColor=color(0,255,0)))
    # slippy.addLayer(googledirections.SlippyLayer(apiKey, a, b, mode='walking', strokeColor=color(0,0,255)))
    # slippy.addLayer(googledirections.SlippyLayer(apiKey, a, b, mode='driving', strokeColor=color(255,0,0)))
    # slippy.addLayer(googledirections.SlippyLayer(apiKey, a, b, mode='transit', strokeColor=color(0,255,255)))
    
    
    # Speculate on routes taken by actual Citibike customers.
    
    # with open('citibike.csv') as f:
    #     reader = csv.reader(f)
    #     header = reader.next()
    
    #     for row in reader:
    #         start_lat = float(row[5])
    #         start_lon = float(row[6])
    #         a = (start_lat, start_lon)
            
    #         end_lat = float(row[9])
    #         end_lon = float(row[10])
    #         b = (end_lat, end_lon)
            
    #         route = googledirections.SlippyLayer(apiKey, a, b, mode='bicycling', strokeColor=color(0,255,0))
    #         slippy.addLayer(route)
    
    
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
    drawExample()
    popMatrix()

    drawGui()


def drawExample():
    # An example of how to draw something in the space of the map.
    stroke(255,0,0)
    noFill()
    
    # Calculate the coordinates of a point in pixel space.
    jfk_y = slippy.latToY(40.6413)
    jfk_x = slippy.lonToX(-73.7781)
    ellipse(jfk_x, jfk_y, 50, 50)
    
    lga_y = slippy.latToY(40.7769)
    lga_x = slippy.lonToX(-73.8740)
    ellipse(lga_x, lga_y, 50, 50)
    
    # Just draw a line between LGA and JFK for fun.
    line(lga_x, lga_y, jfk_x, jfk_y)


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
        print "Exporting the entire map to output/slippymap.png..."
        slippy.save("output/slippymap.png")
        print "Done exporting."
    
    elif key == 'b':
        print "Exporting the basemap only to output/basemap.png..."
        slippy.baseMap.save("output/basemap.png")
        print "Done exporting." 


# --------------------------------------------------------------------------------------
# GUI

def drawGui():
    drawCoordinates()
    drawHelp()

def drawCoordinates():
    noStroke()
    fill(64)
    rect(10, 10, 300, 20)
    
    fill(255)
    lat = slippy.yToLat(mouseY - pan.panY)
    lon = slippy.xToLon(mouseX - pan.panX)

    text(str(lat) + " x " + str(lon), 15, 25)

def drawHelp():
    noStroke()
    fill(64)
    rect(10, height - 29, 400, 20)
    
    fill(255)
    text("+/- to zoom, r to recenter, e to export, b to export the basemap", 15, height - 15)