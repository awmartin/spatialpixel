import gsv

# ---------------------------------------------------------------------------------------
# Parameters

# The CSV file that contains the lat/lon locations. e.g. "locations2.csv"
#
#     Latitude,Longitude
#     40.744312,-73.994425
locations_filename = "sample-locations.csv"

# Create the filename we want to save as, e.g. streetview-2-90.jpg.
# Just change the name before the "-{0}-{1}.jpg"
output_template = "streetview-{0}-{1}.jpg"

# Put your Google StreetView API key here. Should look like: AZzaSyAMw219rAW8zEjzQ2_Fz5FPpx9WIJ7D2H9
api_key = "AZzaSyAMw219rAW8zEjzQ2_Fz5FPpx9WIJ7D2H9"

# ---------------------------------------------------------------------------------------
# Run the code!

streetview = gsv.GoogleStreetViewPhotos(api_key)
streetview.parseLocations(locations_filename)
streetview.getPhotos(output_template)
