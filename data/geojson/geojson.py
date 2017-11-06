import json


class RenderGeoJson(object):
    def __init__(self, fileobj):
        # TODO Accept a json string and dict containing geojson data.
        if isinstance(fileobj, str):
            with open(fileobj) as f:
                self.data = json.load(f)
        elif isinstance(fileobj, file):
            self.data = json.load(f)

        self._elts = []
        self.parse()

    def addelement(self, elt):
        self._elts.append(elt)

    def parse(self):
        for feature in self.data['features']:  # FeatureCollection
            geoType = feature['geometry']['type']
            coords = feature['geometry']['coordinates']

            if geoType == "Polygon":
                self.addelement(GeoJsonPolygon(coords, feature))
            elif geoType == "MultiPolygon":
                self.addelement(GeoJsonMultiPolygon(coords, feature))
            elif geoType == "LineString":
                self.addelement(GeoJsonLineString(coords, feature))
            elif geoType == "Point":
                self.addelement(GeoJsonPoint(coords, feature))
            elif geoType == "GeometryCollection":
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

    def draw(self, lonToX, latToY, pgraphics):
        for linestring in self.linestrings:
            linestring.draw(lonToX, latToY, pgraphics)

class GeoJsonLineString(GeoJsonObject):
    def draw(self, lonToX, latToY, pgraphics):
        s = pgraphics.createShape()
        s.beginShape()

        for pt in self.pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))

        s.endShape()
        pgraphics.shape(s, 0, 0)

class GeoJsonPoint(GeoJsonObject):
    def draw(self, lonToX, latToY, pgraphics):
        lon, lat = self.pt[0], self.pt[1]
        pgraphics.ellipse(lonToX(lon), latToY(lat), 3, 3)
