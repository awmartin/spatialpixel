import json

class Layer(object):
    def __init__(self, filename, strokeColor=color(255,0,0), fillColor=None):
        self.filename = filename
        self.strokeColor = strokeColor
        self.fillColor = fillColor
        
        self.layerObject = RenderGeoJson.open(filename)
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


class RenderGeoJson(object):
    @classmethod
    def open(self, filename):
        with open(filename) as f:
            geojson = RenderGeoJson(f)
        geojson.parse()
        return geojson
    
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

