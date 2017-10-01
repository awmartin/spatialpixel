"""An alternative way to view sample earthquake data."""

import csv

def setup():
    size(1000, 700)

    # This file looks like this:
    # Date,TimeUTC,Latitude,Longitude,Magnitude,Depth
    # 2010/11/02,06:39:55.6,-5.378,151.545,5.8, 41
    # 2010/11/02,03:36:54.2,12.979,-91.224,4.9, 60

    global quakes
    quakes = []
        
    with open("quakes.csv") as f:
        reader = csv.reader(f)
        header = reader.next() # Skip the header row.
        
        x = 0
        for row in reader:
            magnitude = float(row[4])
            
            quake = (x, magnitude)
            quakes.append(quake)
            
            x += 1
    
def draw():
    background(32)
    
    for quake in quakes:
        x, magnitude = quake
        
        if mouseX == x:
            noStroke()
            fill(255,0,0)
            textSize(15)
            text(magnitude, x, height / 2 + 15)
            
            stroke(255, 0, 0)
            strokeWeight(5.0)
        else:
            stroke(144)
            strokeWeight(1.0)

        line(x, height / 2, x, height / 2 - magnitude * 10)

