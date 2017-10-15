import json


def defaultkeyer(feature):
    return None

def defaultstyler(key, feature):
    feature.noFill()
    feature.stroke(255, 0, 0)

class RenderGeoJson(object):
    @classmethod
    def open(self, filename, styler=None, keyer=None):
        with open(filename) as f:
            geojson = RenderGeoJson(f, styler, keyer)
        geojson.parse()
        return geojson

    def __init__(self, file, styler=None, keyer=None):
        self.data = json.load(file)

        # Function that given an id will set the drawing style.
        self.styler = styler if styler is not None else defaultstyler
        # Function that given a data point will return a unique key for the renderable element.
        self.keyer = keyer if keyer is not None else defaultkeyer

        self._elts = []

    def addElement(self, elt):
        self._elts.append(elt)

    def parse(self):
        for feature in self.data['features']:  # FeatureCollection
            key = self.keyer(feature)

            geoType = feature['geometry']['type']
            coords = feature['geometry']['coordinates']

            if geoType == "Polygon":
                for pts in coords:
                    self.addElement(GeoJsonPolygon(pts, key, self.styler))
            elif geoType == "MultiPolygon":
                for polygon in coords:
                    for pts in polygon:
                        self.addElement(GeoJsonPolygon(pts, key, self.styler))
            elif geoType == "LineString":
                self.addElement(GeoJsonLineString(coords, key, self.styler))
            elif geoType == "Point":
                self.addElement(GeoJsonPoint(coords, key, self.styler))

    def render(self, lonToX, latToY, pgraphics):
        for elt in self._elts:
            elt.draw(lonToX, latToY, pgraphics)

    def draw(self, lonToX, latToY):
        pass


class GeoJsonPolygon(object):
    def __init__(self, pts, key=None, styler=None):
        self.pts = pts
        self.key = key
        self.styler = styler if styler is not None else noop

    def draw(self, lonToX, latToY, pgraphics):
        self.styler(self.key, pgraphics)

        s = pgraphics.createShape()
        s.beginShape()

        for pt in self.pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))

        s.endShape(CLOSE)
        pgraphics.shape(s, 0, 0)

class GeoJsonLineString(object):
    def __init__(self, pts, key=None, styler=None):
        self.pts = pts
        self.key = key
        self.styler = styler if styler is not None else noop

    def draw(self, lonToX, latToY, pgraphics):
        self.styler(self.key, pgraphics)

        s = pgraphics.createShape()
        s.beginShape()

        for pt in self.pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))

        s.endShape()
        pgraphics.shape(s, 0, 0)

class GeoJsonPoint(object):
    def __init__(self, pt, key=None, styler=None):
        self.pt = pt
        self.key = key
        self.styler = styler if styler is not None else noop

    def draw(self, lonToX, latToY, pgraphics):
        self.styler(self.key, pgraphics)
        lon, lat = self.pt[0], self.pt[1]
        pgraphics.ellipse(lonToX(lon), latToY(lat), 3, 3)
