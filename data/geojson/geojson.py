import json


class RenderGeoJson(object):
    def __init__(self, data):
        self.data = None

        if isinstance(data, str):
            # Hmm, this could be a filename or a string of JSON data.
            try:
                # Is this a filename? If so, attempt to open the file.
                with open(data, 'r') as f:
                    self.data = json.load(f)
            except:
                # Attempt to load as a JSON string.
                self.data = json.loads(data)

        elif isinstance(data, file):
            # If handed a file object, just read it.
            self.data = json.load(data)

        elif isinstance(data, dict):
            # Assume this is raw GeoJSON.
            # TODO Validate GeoJSON format.
            self.data = data

        self._elts = []
        self.parse()

    def add_element(self, elt):
        self._elts.append(elt)

    @property
    def elements(self):
        return self._elts or []

    @property
    def features(self):
        if 'features' in self.data:
            return self.data['features'] or []
        return []

    def parse(self):
        for feature in self.features:  # FeatureCollection
            geo_type = feature['geometry']['type']
            coords = feature['geometry']['coordinates']

            if geo_type == "Polygon":
                self.add_element(GeoJsonPolygon(coords, feature))
            elif geo_type == "MultiPolygon":
                self.add_element(GeoJsonMultiPolygon(coords, feature))
            elif geo_type == "LineString":
                self.add_element(GeoJsonLineString(coords, feature))
            elif geo_type == "Point":
                self.add_element(GeoJsonPoint(coords, feature))
            elif geo_type == "GeometryCollection":
                # TODO GeometryCollection
                pass

    def render(self, lonToX, latToY, pgraphics, styler=None):
        for elt in self._elts:
            shoulddraw = True

            if styler is not None:
                shoulddraw = styler(elt.data, pgraphics)
                if shoulddraw is None:
                    shoulddraw = True

            if shoulddraw:
                elt.draw(lonToX, latToY, pgraphics)

    def draw(self, lonToX, latToY, styler=None):
        self.render(lonToX, latToY, this, styler)


class GeoJsonObject(object):
    def __init__(self, pts, data=None):
        self.pts = pts
        self.data = data

    @property
    def centroid(self):
        return 0, 0

    def draw(self, lonToX, latToY, pgraphics):
        pass

class GeoJsonMultiPolygon(GeoJsonObject):
    def __init__(self, coords, data=None):
        self.coords = coords
        self.data = data

        self.polygons = []
        for pts in self.coords:
            polygon = GeoJsonPolygon(pts)
            self.polygons.append(polygon)

    @property
    def centroid(self):
        # return self.polygons[0].centroid
        return average([polygon.centroid for polygon in self.polygons])

    def draw(self, lonToX, latToY, pgraphics):
        for polygon in self.polygons:
            polygon.draw(lonToX, latToY, pgraphics)

class GeoJsonPolygon(GeoJsonObject):
    def __init__(self, coords, data=None):
        self.coords = coords
        self.data = data

        self.linestrings = []
        for pts in self.coords:
            linestring = GeoJsonLineString(pts)
            self.linestrings.append(linestring)

    @property
    def centroid(self):
        # According to the spec, the first linestring must be the external outline.
        return self.linestrings[0].centroid

    def draw(self, lonToX, latToY, pgraphics):
        for linestring in self.linestrings:
            linestring.draw(lonToX, latToY, pgraphics)

class GeoJsonLineString(GeoJsonObject):
    @property
    def centroid(self):
        return centroid(self.pts)

    def draw(self, lonToX, latToY, pgraphics):
        s = pgraphics.createShape()
        s.beginShape()

        for pt in self.pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))

        s.endShape()
        pgraphics.shape(s, 0, 0)

class GeoJsonPoint(GeoJsonObject):
    @property
    def centroid(self):
        return self.pts

    def draw(self, lonToX, latToY, pgraphics):
        lon, lat = self.pts[0], self.pts[1]
        pgraphics.ellipse(lonToX(lon), latToY(lat), 3, 3)


def average(pts):
    lon, lat = 0, 0
    for pt in pts:
        lon += pt[0]
        lat += pt[1]
    return lon / len(pts), lat / len(pts)

# https://en.wikipedia.org/wiki/Centroid under "Centroid of a polygon"
def centroid(pts):
    n = len(pts)
    if n == 1:
        return pts[0][0], pts[0][1]

    A = 0
    for i in xrange(0, n - 1):
        A += pts[i][0] * pts[i + 1][1] - pts[i + 1][0] * pts[i][1]
    A *= 0.5

    lon, lat = 0, 0
    for i in xrange(0, n - 1):
        b = (pts[i][0] * pts[i + 1][1] - pts[i + 1][0] * pts[i][1])
        lon += (pts[i][0] + pts[i + 1][0]) * b
        lat += (pts[i][1] + pts[i + 1][1]) * b

    return lon / (6 * A), lat / (6 * A)
