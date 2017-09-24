import csv
import urllib

# Open the file, grab the lat and lon values as floats,
# and store in the "locations" array.

locations = []
with open('locations.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)

    is_first_row = True
    for row in reader:
        # Skip the first row.
        if is_first_row:
            is_first_row = False
            continue

        lat, lon = float(row[0]), float(row[1])
        location = (lat, lon)
        locations.append(location)

# Put your Google Street View API key here.
api_key = "xxxxxxxx"

api_url = "https://maps.googleapis.com/maps/api/streetview?size=640x400&location={0},{1}&fov=90&heading={2}&pitch=10&key={3}"
row = 2
headings = [0, 90, 180, 270]

# Loop over every location, and for each location, loop over all the possible headings.
for location in locations:
    for direction in headings:
        # Create the URL for the request to Google.
        lat, lon = location
        url = api_url.format(lat, lon, direction, api_key)

        # Create the filename we want to save as, e.g. location-2-90.jpg.
        filename = "location-{0}-{1}.jpg".format(row, direction)

        # Use the 'curl' command to actually make the request and save the file to disk.
        urllib.urlretrieve(url, filename)
        print "Got %s" % (filename,)

    # Increment the row to correlate with the Excel file.
    row += 1
    
print "Done"