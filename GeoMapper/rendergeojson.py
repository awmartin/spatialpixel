import json

class RenderGeoJson(object):
    data = None
    
    def __init__(self, file):
        self.data = json.load(file)
    
    def draw(self, lonToX, latToY):
        for feature in self.data['features']:
            geoType = feature['geometry']['type']
            coords = feature['geometry']['coordinates']

            if geoType == "Polygon":
                for pts in coords:
                    self.drawPolygon(pts, lonToX, latToY)
            elif geoType == "MultiPolygon":
                for polygon in coords:
                    for pts in polygon:
                        self.drawPolygon(pts, lonToX, latToY)
            elif geoType == "LineString":
                self.drawLineString(coords, lonToX, latToY)

    def drawPolygon(self, pts, lonToX, latToY):
        s = createShape()
        s.beginShape()
        
        for pt in pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))

        s.endShape(CLOSE)
        shape(s, 0, 0)
    
    def drawLineString(self, pts, lonToX, latToY):
        s = createShape()
        s.beginShape()
        
        for pt in pts:
            lon, lat = pt[0], pt[1]
            s.vertex(lonToX(lon), latToY(lat))
            
        s.endShape()
        shape(s, 0, 0)
