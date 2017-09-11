# Size the map arbitrarily.
size(800, 500)

# Set a white background, black stroke color, and don't fill shapes.
background(255, 255, 255)

# Let's load an image of a map from the Internet and get some info about it.
map = loadImage("https://raw.githubusercontent.com/awmartin/spatialpixel/master/Assets/Maps/BlankMap-Equirectangular-720px.png")
print map.width, map.height

# Hmm, looks like it's 720px pixels wide and 360px pixels tall. Let's see what that looks like:
image(map, 0, 0)

# Note that this is a "cylindrical equirectangular" projection, meaning that an area of 
# 1º of latitude by 1º of longitude is square, so it maps rather well to pixels, which are 
# also square. Other map projections won't work as simply as this technique below.
# It's also called a cylindrical equidistant projection.

# Ok, interesting.
# In Processing, the x pixels of an image go from 0 to 720, but longitude goes from -180 to 180.
# Also, latitude goes from  90 in the North Pole to -90 in the South Pole, but y- space goes
# from 0 in the north to 360 at the south.
# Let's figure out if we can map longitude and latitude to x- and y-pixel space.

# First, a frame of reference.
# Tell Processing you want to draw rectangles by specifying corner coordinates.
rectMode(CORNERS)
# Set a light gray stroke color and don't fill the shapes.
stroke(192, 192, 192)
noFill()

# Draw the rectangle that represents longitude and latitude coordinate boundaries.
rect(-180, -90, 180, 90)

# Ok, bit it's not centered, is it? Let's move the map 360 pixels to the right and
# 180 pixels down, effectively half the size of the map, to center our rectangle.
translate(map.width / 2, map.height / 2)

# Ideally, we'd like to draw in longitude and latitude coordinates.
# Luckily, longitude spans 360 degrees, and our map is 720px wide.
# Also, latitude spans 180 degrees, and our map is 360 pixels tall.
# Sounds like if we double the size of our rectangle, it might fit the map.
scale(2)
# Scaling up will also scale the shape stroke size, so let's ensure the stoke
# width is the original, just for looks.
strokeWeight(0.5)

# Draw the rectangle that represents longitude and latitude coordinate boundaries.
rect(-180, -90, 180, 90)
# For good measure, also draw the equator...
line(-180, 0, 180, 0)
# and the prime meridian.
line(0, -90, 0, 90)

# Now draw NYC to see what happens: 40.7128° N, 74.0059° W
stroke(255, 0, 0)  # Red
ellipse(-74.059, 40.7128, 3, 3)

# Hmm, that doesn't seem right. New York is in the northern hemisphere.
# The problem is what we saw before, that the y values increase down the 
# sketch canvas, but that's the opposite direction of what latitude does.
# Let's scale the y values by -1 to reverse the direction.
scale(1, -1)

# Try to draw NYC again.
stroke(0, 255, 0)  # Green
ellipse(-74.059, 40.7128, 3, 3)
# That looks right.

# Here's London, just to be sure: 51.5074° N, 0.1278° W
ellipse(0.1278, 51.5074, 3, 3)

# And Cape Town: 33.9249° S, 18.4241° E
ellipse(18.4241, -33.9249, 3, 3)

# And Sydney: 33.8688° S, 151.2093° E
ellipse(151.2093, -33.8688, 3, 3)

