# include the third-party libraries selectively
import sys, os, imp
separator = os.path.sep
root = os.path.dirname(__file__)

# Currently, the only function needed is decode_polyline from googlemaps.convert.
# Importing like this sidesteps importing the "requests" library required by
# googlemaps.client, which likely doesn't work with processing.py yet.
libpath = os.path.join(root, "googlemaps", "services", "googlemaps", "convert.py")
googlemaps_convert = imp.load_source("googlemaps_convert", libpath)
import googlemaps_convert
