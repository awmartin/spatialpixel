import json


def defaultstyler(key, feature, data):
    feature.noFill()
    feature.stroke(255, 0, 0)

class RenderGeoJson(object):
    @classmethod
    def open(self, filename, styler=None):
        with open(filename) as f:
            geojson = RenderGeoJson(f, styler)
        geojson.parse()
        return geojson

    def __init__(self, file, styler=None):
        self.data = json.load(file)

        # Function that given an id will set the drawing style.
        self.styler = styler if styler is not None else defaultstyler

        self._elts = []

    def addElement(self, elt):
        self._elts.append(elt)

    def parse(self):
        for feature in self.data['features']:  # FeatureCollection
            geoType = feature['geometry']['type']
            coords = feature['geometry']['coordinates']

            if geoType == "Polygon":
                for pts in coords:
                    self.addElement(GeoJsonPolygon(pts, feature, self.styler))
            elif geoType == "MultiPolygon":
                for polygon in coords:
                    for pts in polygon:
                        self.addElement(GeoJsonPolygon(pts, feature, self.styler))
            elif geoType == "LineString":
                self.addElement(GeoJsonLineString(coords, feature, self.styler))
            elif geoType == "Point":
                self.addElement(GeoJsonPoint(coords, feature, self.styler))

    def render(self, lonToX, latToY, pgraphics):
        for elt in self._elts:
            elt.draw(lonToX, latToY, pgraphics)

    def draw(self, lonToX, latToY):
        pass


class GeoJsonPolygon(object):
    def __init__(self, pts, data=None, styler=None):
        self.pts = pts
        self.data = data
        self.styler = styler if styler is not None else noop

    def draw(self, lonToX, latToY, pgraphics):
        self.styler(self.data, pgraphics)

        s = pgraphics.createShape()
        s.beginShape()

        for pt in self.pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))

        s.endShape(CLOSE)
        pgraphics.shape(s, 0, 0)

class GeoJsonLineString(object):
    def __init__(self, pts, data=None, styler=None):
        self.pts = pts
        self.data = data
        self.styler = styler if styler is not None else noop

    def draw(self, lonToX, latToY, pgraphics):
        self.styler(self.data, pgraphics)

        s = pgraphics.createShape()
        s.beginShape()

        for pt in self.pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))

        s.endShape()
        pgraphics.shape(s, 0, 0)

class GeoJsonPoint(object):
    def __init__(self, pt, data=None, styler=None):
        self.pt = pt
        self.data = data
        self.styler = styler if styler is not None else noop

    def draw(self, lonToX, latToY, pgraphics):
        self.styler(self.data, pgraphics)
        lon, lat = self.pt[0], self.pt[1]
        pgraphics.ellipse(lonToX(lon), latToY(lat), 3, 3)
