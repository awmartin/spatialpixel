import xml.etree.ElementTree as ET


def defaultkeyer(feature):
    return None

def defaultstyler(key, feature):
    feature.noFill()
    feature.stroke(255, 0, 0)

class RenderKML(object):
    @classmethod
    def open(self, filename, styler=None, keyer=None):
        with open(filename) as f:
            kml = RenderKML(f, styler=styler, keyer=keyer)
        kml.parse()
        return kml

    def __init__(self, xmlfile, styler=None, keyer=None):
        self.tree = ET.parse(xmlfile)

        self.styler = styler if styler is not None else defaultstyler
        self.keyer = keyer if keyer is not None else defaultkeyer

        self.placemarks = []

    def render(self, lonToX, latToY, pgraphics):
        for placemark in self.placemarks:
            self.styler(placemark.key, pgraphics)
            placemark.draw(lonToX, latToY, pgraphics)

    def draw(self, lonToX, latToY):
        for placemark in self.placemarks:
            self.styler(placemark.key, pgraphics)
            placemark.draw(lonToX, latToY, this)

    def parse(self):
        root = self.tree.getroot()  # <kml>
        for document in root:  # <Document>
            for subitem in document:  # subitem == <Placemark> or <Folder>
                if subitem.tag.endswith("Placemark"):
                    self.parse_placemark(subitem)
                elif subitem.tag.endswith("Folder"):
                    for child in subitem:
                        if child.tag.endswith("Placemark"):
                            self.parse_placemark(child)

    # https://developers.google.com/kml/documentation/kmlreference#placemark
    def parse_placemark(self, placemark):
        key = self.keyer(placemark)
        self.placemarks.append(KmlPlacemark(placemark, key))


class KmlPlacemark(object):
    def __init__(self, placemark, key):
        self.placemark = placemark
        self.key = key

        self.children = []
        self.parse()

    def parse(self):
        for child in self.placemark:
            geometry = KmlGeometry.parse(child)
            if geometry is not None:
                self.children.append(geometry)

    def draw(self, lonToX, latToY, pgraphics):
        for child in self.children:
            child.draw(lonToX, latToY, pgraphics)


# https://developers.google.com/kml/documentation/kmlreference#geometry
class KmlGeometry(object):
    @classmethod
    def parse(self, geometry):
        if geometry.tag.endswith("Point"):
            return KmlPoint(geometry)

        elif geometry.tag.endswith("LineString"):
            return KmlLineString(geometry)

        elif geometry.tag.endswith("LinearRing"):
            return KmlLinearRing(geometry)

        elif geometry.tag.endswith("Polygon"):
            return KmlPolygon(geometry)

        elif geometry.tag.endswith("MultiGeometry"):
            return KmlMultiGeometry(geometry)

        elif geometry.tag.endswith("Track"):   # gx:Track ??
            return KmlTrack(geometry)

        return None


class KmlPolygon(object):
    def __init__(self, element):
        self.element = element
        self.outer = []
        self.inner = []
        self.parse()

    def draw(self, lonToX, latToY, pgraphics):
        # TODO Make Polygon rendering do the right thing with holes.
        for child in self.outer:
            child.draw(lonToX, latToY, pgraphics)
        for child in self.inner:
            child.draw(lonToX, latToY, pgraphics)

    # https://developers.google.com/kml/documentation/kmlreference#polygon
    def parse(self):
        for child in self.element:
            if child.tag.endswith("outerBoundaryIs"):
                # https://developers.google.com/kml/documentation/kmlreference#outerboundaryis
                for subchild in child:
                    geometry = KmlGeometry.parse(subchild)
                    if geometry is not None:
                        self.outer.append(geometry)
            elif child.tag.endswith("innerBoundaryIs"): # Can have multiple ones.
                # https://developers.google.com/kml/documentation/kmlreference#innerboundaryis
                for subchild in child:
                    geometry = KmlGeometry.parse(child)
                    if geometry is not None:
                        self.inner.append(geometry)


class KmlMultiGeometry(object):
    def __init__(self, element):
        self.element = element
        self.geometries = []
        self.parse()

    def draw(self, lonToX, latToY, pgraphics):
        for geometry in self.geometries:
            geometry.draw(lonToX, latToY, pgraphics)

    def parse(self):
        for child in self.element:
            geometry = KmlGeometry.parse(child)
            if geometry is not None:
                self.geometries.append(geometry)


class KmlLineString(object):
    def __init__(self, element):
        self.element = element
        self.points = []
        self.parse()

    def draw(self, lonToX, latToY, pgraphics):
        s = pgraphics.createShape()
        s.beginShape()
        for pt in self.points:
            x = lonToX(pt[0])
            y = latToY(pt[1])
            s.vertex(x, y)
        s.endShape()
        pgraphics.shape(s, 0, 0)

    def parse(self):
        for subchild in self.element:
            if subchild.tag.endswith("coordinates"):
                coordinates_text = subchild.text
                self.points = parse_coordinates(coordinates_text)


class KmlLinearRing(object):
    def __init__(self, element):
        self.element = element
        self.points = []
        self.parse()

    def draw(self, lonToX, latToY, pgraphics):
        s = pgraphics.createShape()
        s.beginShape()
        for pt in self.points:
            x = lonToX(pt[0])
            y = latToY(pt[1])
            s.vertex(x, y)
        s.endShape(pgraphics.CLOSE)
        pgraphics.shape(s, 0, 0)

    def parse(self):
        for subchild in self.element:
            if subchild.tag.endswith("coordinates"):
                coordinates_text = subchild.text
                self.points = parse_coordinates(coordinates_text)


class KmlTrack(object):
    def __init__(self, element):
        self.element = element
        self.waypoints = []
        self.parse()

    def draw(self, lonToX, latToY, pgraphics):
        for waypoint in self.waypoints:
            waypoint.draw(lonToX, latToY, pgraphics)

    def parse(self):
        for entry in self.element:
            tag = entry.tag.strip()
            if tag.endswith("AltitudeMode"):
                pass
            elif tag.endswith("when"):
                pass
            elif tag.endswith("coord"):
                pt = parse_lonlat(entry.text, separator=" ")
                self.waypoints.append(KmlWayPoint(pt))


class KmlWayPoint(object):
    def __init__(self, lonlat):
        self.lonlat = lonlat

    def draw(self, lonToX, latToY, pgraphics):
        x = lonToX(self.lonlat[0])
        y = latToY(self.lonlat[1])
        pgraphics.ellipse(x, y, 5, 5)


class KmlPoint(object):
    def __init__(self, element):
        self.element = element
        self.pt = None
        self.parse()

    def draw(self, lonToX, latToY, pgraphics):
        x = lonToX(self.pt[0])
        y = latToY(self.pt[1])
        pgraphics.ellipse(x, y, 5, 5)

    def parse(self):
        for child in self.element:
            if child.tag.endswith("coordinates"):
                points = parse_coordinates(child.text)
                self.pt = points[0]

def parse_coordinates(coordinates_text):
    points_text = coordinates_text.strip().split(" ")
    return map(parse_lonlat, points_text)

def parse_lonlat(point_text, separator=","):
    params = point_text.split(separator)
    return (float(params[0]), float(params[1]))
