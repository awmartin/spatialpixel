"""This script pulls Google StreetView images from their API given a CSV file of locations
specified as latitude/longitude pairs.

To use this, you'll need to sign up for a Google StreetView API key and provide it at the
bottom of the file along with other parameters needed to run this script.

You can also include this file as a module in other Processing sketches or Python scripts.

"""

import urllib
import csv


class GoogleStreetViewPhotos(object):
    locations = None
    api_key = None
    csvdialect = None
    has_header_row = False

    def __init__(self, api_key):
        self.locations = []
        self.api_key = api_key

    def addLatLon(self, lat, lon):
        self.locations.append((lat, lon))

    def addLocation(self, location):
        self.locations.append(location)

    def provideLocations(self, locations):
        self.locations = locations

    def parseLocations(self, filename):
        # Open the file and parse it with the csv.reader method.
        with open(filename, 'rb') as csvfile:
            # Gather some information about the CSV file.
            csvsample = csvfile.read(1024)
            csvfile.seek(0)
            self.csvdialect = csv.Sniffer().sniff(csvsample)
            self.has_header_row = csv.Sniffer().has_header(csvsample)

            # Now, set up an object that will enable us to read the CSV file one row at a time.
            reader = csv.reader(csvfile, self.csvdialect)

            # Iterate over all the rows, converting the first elements of each row to floats.
            # If we're looking at the first row, and the CSV file has a header row, skip it for now.
            is_first_row = True
            for row in reader:
                if self.has_header_row and is_first_row:
                    is_first_row = False
                    continue

                # This assumes the first column is latitude and the second is longitude.
                lat, lon = float(row[0]), float(row[1])

                # Store all the locations as tuples of (latitude, longitude)
                location = (lat, lon)
                self.addLocation(location)

    def getPhotos(self, template):
        if len(self.locations) == 0:
            print "This doesn't have any locations available. " + \
                "You can either provide a file with parseLocations() or " + \
                "add locations manually with addLocation()."
            return

        # Prepare the URL template.
        # TODO: Parameterize this.
        url_template = "https://maps.googleapis.com/maps/api/streetview" + \
            "?size=640x400" + \
            "&location={0},{1}" + \
            "&fov=90" + \
            "&heading={2}" + \
            "&pitch=10" + \
            "&key={3}"

        row = 2 if self.has_header_row else 1
        headings = [0, 90, 180, 270]

        # Loop over every location, and for each location, loop over all the possible headings.
        for location in self.locations:
            for dir in headings:
                # Create the URL for the request to Google.
                lat, lon = location
                url = url_template.format(lat, lon, dir, self.api_key)

                # Create the filename as well.
                filename = template.format(row, dir)

                # Use urllib.urlretrieve to send the request and save the response to a file.
                # TODO: Generalize this so a user can get a PImage or write the file or whatever.
                urllib.urlretrieve(url, filename)

            # Increment the row to correlate with the row number in the CSV file.
            row += 1
