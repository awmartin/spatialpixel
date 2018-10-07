# This demo uses the OpenStreetMap library in SpatialPixel to query for and render street data.

import spatialpixel.mapping.slippymapper as slippy
import spatialpixel.mapping.openstreetmap as osm


def setup():
    size(1000, 600)

    # Create a SlippyMapper object. The default location is midtown Manhattan.
    global city
    city = slippy.SlippyMapper(40.7517555796, -73.9883241272, 15, 'carto-dark', width, height)
    
    # Create an OSM object that lets us express a query.
    streets = osm.OpenStreetMap(bbox=city.bounding_box)
    highway_types = [
        'motorway', 'motorway_link',
        'trunk', 'trunk_link',
        'primary', 'primary_link',
        'secondary', 'secondary_link',
        'tertiary', 'tertiary_link',
        'unclassified',
        'residential',
        'living_street',
        'service'
        ]
    
    # Create a "Way" object to query for individual highway segments.
    streets.add(osm.Way({'highway': highway_types}))

    # Actually perform the request. This may take a few seconds.
    streets.request()


    # A function that defines how to render a given feature object returned by the query.
    def styler(feature, graphics):
        if feature['type'] == 'way':
            graphics.noFill()
            graphics.strokeWeight(2)

            if feature['tags']['highway'] in ('motorway', 'trunk', 'motorway_link', 'trunk_link'):
                graphics.strokeWeight(4)
                graphics.stroke(255, 192, 192)

            elif feature['tags']['highway'] in ('primary', 'primary_link'):
                graphics.strokeWeight(3)
                graphics.stroke(255, 192, 192)

            elif feature['tags']['highway'] in ('secondary', 'secondary_link'):
                graphics.stroke(255, 128, 128)

            elif feature['tags']['highway'] in ('tertiary', 'tertiary_link'):
                graphics.stroke(192, 64, 64)

            else:
                graphics.stroke(96, 0, 0)

            return True

        else:
            return False

    # Add the street object to our map by wrapping it in a SlippyLayer object.    
    city.addLayer(osm.SlippyLayer(streets, styler=styler))

    # Render the city.
    city.render()

def draw():
    background(0)
    city.draw()
