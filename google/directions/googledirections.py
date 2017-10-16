import httplib
import json

from ...third_party import googlemaps_convert


class RenderGoogleDirections(object):
    def __init__(self, api_key):
        self.api_key = api_key

        self.locations = []

    def request(self, start_location, end_location, mode="driving"):
        """Make a request to the API. locations are tuples of (lat, lon) format.

        Possible modes are 'driving', 'bicycling', 'walking', 'transit'.
        """

        host = "maps.googleapis.com"

        start_param = str(start_location[0]) + "," + str(start_location[1])
        end_param = str(end_location[0]) + "," + str(end_location[1])

        api_url = "/maps/api/directions/json?origin={1}&destination={2}&mode={3}&key={0}"
        url = api_url.format(self.api_key, start_param, end_param, mode)

        # Assumes everything goes just peachy.

        conn = httplib.HTTPSConnection(host)
        conn.request("GET", url)
        res = conn.getresponse()
        response_data = res.read()

        self.data = json.loads(response_data)
        self.steps = []

        try:
            # TOOD Ensure we're getting all the routes and legs if necessary.
            self.steps = self.data["routes"][0]["legs"][0]["steps"]
        except:
            print "Google driving directions didn't load properly for some reason. For now, just try again."

        conn.close()

        self.get_locations()

    def render(self, lonToX, latToY, pgraphics):
        s = pgraphics.createShape()
        s.beginShape()

        def vertex(location):
            x = lonToX(float(location['lng']))
            y = latToY(float(location['lat']))
            s.vertex(x, y)

        for loc in self.locations:
            vertex(loc)

        s.endShape(LINES)
        pgraphics.shape(s, 0, 0)

    def draw(self):
        pass

    def get_locations(self):
        for step in self.steps:
            self.add_location(step['start_location'])

            # Decoded polyline here.
            if 'polyline' in step:
                polyline = step['polyline']
                if 'points' in polyline:
                    points_str = str(polyline['points'])
                    if len(points_str) > 0:
                        path = googlemaps_convert.decode_polyline(points_str)
                        for loc in path:
                            self.add_location(loc)

            self.add_location(step['end_location'])

    def add_location(self, loc):
        self.locations.append(loc)
