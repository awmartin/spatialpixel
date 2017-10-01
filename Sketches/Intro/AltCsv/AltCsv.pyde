"""An alternative way to view sample earthquake data."""

import csv

size(1000, 700)

background(32)
stroke(144)

# This file looks like this:
# Date,TimeUTC,Latitude,Longitude,Magnitude,Depth
# 2010/11/02,06:39:55.6,-5.378,151.545,5.8, 41
# 2010/11/02,03:36:54.2,12.979,-91.224,4.9, 60

with open("quakes.csv") as f:
    reader = csv.reader(f)
    header = reader.next() # Skip the header row.
    
    x = 0
    for row in reader:
        magnitude = float(row[4])
        line(x, height / 2, x, height / 2 - magnitude * 10)
        x += 1
