import json

class RenderGeoJson(object):
    def __init__(self, file):
        self.data = json.load(file)
        
        self._elts = []
    
    def addElement(self, elt):
        self._elts.append(elt)
    
    def parse(self):
        for feature in self.data['features']:
            geoType = feature['geometry']['type']
            coords = feature['geometry']['coordinates']

            if geoType == "Polygon":
                for pts in coords:
                    self.addElement(GeoJsonPolygon(pts))
            elif geoType == "MultiPolygon":
                for polygon in coords:
                    for pts in polygon:
                        self.addElement(GeoJsonPolygon(pts))
            elif geoType == "LineString":
                self.addElement(GeoJsonLineString(coords))
    
    def render(self, lonToX, latToY, pgraphics):
        for elt in self._elts:
            elt.draw(lonToX, latToY, pgraphics)
    
    def draw(self, lonToX, latToY):
        pass


class GeoJsonPolygon(object):
    def __init__(self, pts):
        self.pts = pts
        
    def draw(self, lonToX, latToY, pgraphics):
        s = pgraphics.createShape()
        s.beginShape()
        
        for pt in self.pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))

        s.endShape(CLOSE)
        pgraphics.shape(s, 0, 0)

class GeoJsonLineString(object):
    def __init__(self, pts):
        self.pts = pts
    
    def draw(self, lonToX, latToY, pgraphics):
        s = pgraphics.createShape()
        s.beginShape()
        
        for pt in self.pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))
            
        s.endShape()
        pgraphics.shape(s, 0, 0)


