"""Provides an example of reading a CSV file and storing the data in a list
so you can make interactive visualizations using draw().
"""

import csv

def setup():
    size(1000, 700)

    global worldmap
    worldmap = loadImage("https://raw.githubusercontent.com/awmartin/spatialpixel/master/Assets/Maps/BlankMap-Equirectangular-720px.png")
    
    global quakes
    quakes = []

    # This file looks like this:
    # Date,TimeUTC,Latitude,Longitude,Magnitude,Depth
    # 2010/11/02,06:39:55.6,-5.378,151.545,5.8, 41
    # 2010/11/02,03:36:54.2,12.979,-91.224,4.9, 60
    
    with open("quakes.csv") as f:
        reader = csv.reader(f)
        header = reader.next() # Skip the header row.
        
        for row in reader:
            lon = float(row[3])
            lat = float(row[2])
            magnitude = float(row[4])
            
            # Pack the values we need into a "tuple" and add to the list.
            quake = (lon, lat, magnitude)
            quakes.append(quake)

def draw():
    background(255)

    # Center the world map.
    worldmapX = (width - worldmap.width) / 2
    worldmapY = (height - worldmap.height) / 2
    image(worldmap, worldmapX, worldmapY)
    
    for quake in quakes:
        # Unpack the tuple to get the values we need, then draw the quake.
        lon, lat, magnitude = quake
        
        # Instead of using transformations, map our lat/long values to the
        # min and max dimensions of the worldmap. This makes it easier to
        # compare to the mouse position.
        x = map(lon, -180, 180, worldmapX, worldmapX + worldmap.width)
        
        # Map the y-values backwards because it's upside-down otherwise!
        y = map(lat, -90, 90, worldmapY + worldmap.height, worldmapY) 
        
        # Highlight the quakes that the mouse hovers over.
        distanceToMouse = dist(x, y, mouseX, mouseY)
        if distanceToMouse < magnitude * 2:
            stroke(0, 255, 0)
            fill(0, 255, 0)
        else:
            stroke(255, 0, 0, 64)
            noFill()
        
        ellipse(x, y, magnitude * 4, magnitude * 4)

