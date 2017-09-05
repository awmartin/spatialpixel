import xml.etree.ElementTree as ET

class RenderKML(object):
    tree = None
    
    elts = None
    
    def __init__(self, xmlfile):
        self.tree = ET.parse(xmlfile)
        self.elts = []
        
        self.parse()
    
    def parse(self):
        root = self.tree.getroot()
        for item in root:
            for subitem in item:
                if subitem.tag.endswith("Placemark"):
                    self.parsePlacemark(subitem)
    
    def parsePlacemark(self, placemark):
        for child in placemark:
            if child.tag.endswith("LineString"):
                self.parseLineString(child)
    
    def parseLineString(self, lineString):
        for subchild in lineString:
            if subchild.tag.endswith("coordinates"):
                coordinates_text = subchild.text
                points = self.parseCoordinates(coordinates_text)
                self.elts.append(LineString(points))
    
    def parseCoordinates(self, coordinates_text):
        points_text = coordinates_text.strip().split(" ")
        return map(self.parsePoint, points_text)

    def parsePoint(self, point_text):
        params = point_text.split(",")
        return (float(params[0]), float(params[1]))

    def draw(self, lonToX, latToY):
        for elt in self.elts:
            elt.draw(lonToX, latToY)

class LineString(object):
    points = None
    
    def __init__(self, points):
        self.points = points
    
    def draw(self, lonToX, latToY):
        s = createShape()
        s.beginShape()
        for pt in self.points:
            s.vertex(lonToX(pt[0]), latToY(pt[1]))
        s.endShape()
        shape(s, 0, 0)
