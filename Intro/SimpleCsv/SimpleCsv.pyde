import csv

size(1000, 700)
background(255)
fill(255, 0, 0)
noStroke()

 
worldmap = loadImage("https://raw.githubusercontent.com/awmartin/spatialpixel/master/Assets/Maps/BlankMap-Equirectangular-720px.png")
image(worldmap, (width - worldmap.width)/2, (height - worldmap.height)/2)
print worldmap.width, worldmap.height


translate(width / 2, height / 2)
scale(2, -2)

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
        
        ellipse(lon, lat, 2, 2)
