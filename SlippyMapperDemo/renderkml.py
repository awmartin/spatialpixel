import xml.etree.ElementTree as ET

class Layer(object):
    def __init__(self, filename, strokeColor=color(255,0,0), fillColor=None):
        self.filename = filename
        self.strokeColor = strokeColor
        self.fillColor = fillColor
        
        self.layerObject = RenderKML.open(filename)
        self.underlayMap = None
    
    def setUnderlayMap(self, geomap):
        self.underlayMap = geomap

    def render(self):
        self.layer = createGraphics(self.underlayMap.w, self.underlayMap.h)
        self.layer.beginDraw()
        
        if self.fillColor is not None:
            self.layer.fill(self.fillColor)
        else:
            self.layer.noFill()
        
        if self.strokeColor is not None:
            self.layer.stroke(self.strokeColor)
        else:
            self.layer.noStroke()    
        
        self.layerObject.render(self.underlayMap.lonToX, self.underlayMap.latToY, self.layer)
        
        self.layer.endDraw()
    
    def draw(self):
        image(self.layer, 0, 0)


class RenderKML(object):
    @classmethod
    def open(self, filename):
        with open(filename) as f:
            kml = RenderKML(f)
        kml.parse()
        return kml
        
    def __init__(self, xmlfile):
        self.tree = ET.parse(xmlfile)
        self.elts = []
    
    def parse(self):
        root = self.tree.getroot()  # <kml>
        for item in root:  # <Document>
            for subitem in item:  # <Placemark>
                if subitem.tag.endswith("Placemark"):
                    self.parsePlacemark(subitem)
    
    def parsePlacemark(self, placemark):
        for child in placemark:
            if child.tag.endswith("LineString"):
                self.parseLineString(child)
            if child.tag.endswith("Track"):
                self.parseTrack(child)
    
    def parseLineString(self, lineString):
        for subchild in lineString:
            if subchild.tag.endswith("coordinates"):
                coordinates_text = subchild.text
                points = self.parseCoordinates(coordinates_text)
                self.elts.append(KmlLineString(points))
    
    def parseCoordinates(self, coordinates_text):
        points_text = coordinates_text.strip().split(" ")
        return map(self.parsePoint, points_text)

    def parsePoint(self, point_text, separator=","):
        params = point_text.split(separator)
        return (float(params[0]), float(params[1]))
    
    def parseTrack(self, track):
        for entry in track:
            tag = entry.tag.strip()
            if tag.endswith("AltitudeMode"):
                pass
            elif tag.endswith("when"):
                pass
            elif tag.endswith("coord"):
                pt = self.parsePoint(entry.text, separator=" ")
                self.elts.append(KmlWayPoint(pt))
    
    def render(self, lonToX, latToY, pgraphics):
        for elt in self.elts:
            elt.draw(lonToX, latToY, pgraphics)

    def draw(self, lonToX, latToY):
        for elt in self.elts:
            elt.draw(lonToX, latToY)

class KmlLineString(object):
    def __init__(self, points):
        self.points = points
    
    def draw(self, lonToX, latToY, pgraphics):
        s = pgraphics.createShape()
        s.beginShape()
        for pt in self.points:
            x = lonToX(pt[0])
            y = latToY(pt[1])
            s.vertex(x, y)
        s.endShape()
        pgraphics.shape(s, 0, 0)

class KmlWayPoint(object):
    def __init__(self, pt):
        self.pt = pt
    
    def draw(self, lonToX, latToY, pgraphics):
        x = lonToX(self.pt[0])
        y = latToY(self.pt[1])
        pgraphics.ellipse(x, y, 5, 5)

