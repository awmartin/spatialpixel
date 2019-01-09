# A simple OpenStreetMap demo that requests bicycle paths from the OSM API and renders them.

import spatialpixel.mapping.slippymapper as slippy
import spatialpixel.mapping.openstreetmap as osm

def setup():
    size(1000, 600)

    global city
    # city = slippy.SlippyMapper(55.6800, 12.5778, 14, 'carto-light', width, height)     # Copenhagen
    city = slippy.SlippyMapper(52.377205, 4.898622, 14, 'carto-light', width, height)  # Amsterdam

    # Create an OpenStreetMap object to represent the query to the API.
    # This specifies a bounding box in lat-lon coordinates that that scopes the query to the map.
    bicycle_paths = osm.OpenStreetMap(bbox=city.bounding_box)

    # The challenge with OpenStreetMap data is there are multiple ways to tag the same kind of data.
    # Here, to get paths where bicycles primarily traverse, we need to request three different
    # kinds of data from the API.
    bicycle_paths.add(osm.Relation({'route': 'bicycle'}))
    bicycle_paths.add(osm.Way({'highway': 'cycleway'}))
    bicycle_paths.add(osm.Way({'highway': 'path', 'bicycle': 'designated'}))

    # Sends the request. Might take a few seconds.
    bicycle_paths.request()

    # Add the layer to the map and render.
    city.addLayer(osm.SlippyLayer(bicycle_paths))
    city.render()

def draw():
    background(0)
    city.draw()
