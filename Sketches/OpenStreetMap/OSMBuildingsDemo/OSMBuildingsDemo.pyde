import spatialpixel.mapping.slippymapper as slippy
import spatialpixel.mapping.openstreetmap as osm

def setup():
    size(1000, 600)

    global city
    city = slippy.SlippyMapper(40.751710877894276, -73.9864243877411, 18) # NYC
    city.setServer(None) # Don't include an underlying tile map.
    city.setSize(width, height)

    # Create a new map.
    buildings = osm.OpenStreetMap(bbox=city.bounding_box)
    # Add a request that just looked for way[building].
    buildings.add(osm.Way('building'))
    buildings.request()

    def fill_by_height(feature, pgraphics):
        if feature['type'] != 'way':
            # Don't bother with nodes or other types yet.
            return False

        # Shade the building outline according to height.
        # Sometimes buildings are tagged with number of "levels" and others
        # with an explicit "height" in meters.
        if 'tags' in feature and 'building:levels' in feature['tags']:
            levels = int(feature['tags']['building:levels'])
            r = min(levels * 10, 255)
            pgraphics.fill(255, 255 - r, 255 - r)
        elif 'tags' in feature and 'height' in feature['tags']:
            height = float(feature['tags']['height'])
            levels = height / 3.0
            r = min(levels * 10.0, 255)
            pgraphics.fill(255, 255 - r, 255 - r)
        else:
            pgraphics.noFill()

        pgraphics.stroke(255, 0, 0)
        return True

    # Add the layer and provide the function above for the styler.
    city.addLayer(osm.SlippyLayer(buildings, fill_by_height))
    city.render()

def draw():
    background(255)
    city.draw()
