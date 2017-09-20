import httplib
import json

class Layer(object):
    def __init__(self, apiKey, startLocation, endLocation, mode='driving', strokeColor=color(255,0,0), fillColor=None):
        self.apiKey = apiKey
        self.startLocation = startLocation
        self.endLocation = endLocation
        self.mode = mode
        self.strokeColor = strokeColor
        self.fillColor = fillColor
        
        self.layerObject = GoogleDirections(apiKey)
        self.underlayMap = None
        
        self.layerObject.request(self.startLocation, self.endLocation, self.mode)
    
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

class GoogleDirections(object):
    def __init__(self, api_key):
        self.api_key = api_key
    
    def request(self, start_location, end_location, mode="driving"):
        """Make a request to the API. locations are tuples of (lat, lon) format.
        
        Possible modes are 'driving', 'bicycling', 'walking', 'transit'.
        """
        
        host = "maps.googleapis.com"
        
        start_param = str(start_location[0]) + "," + str(start_location[1])
        end_param = str(end_location[0]) + "," + str(end_location[1])
        
        api_url = "/maps/api/directions/json?origin={1}&destination={2}&mode={3}&key={0}"
        url = api_url.format(self.api_key, start_param, end_param, mode)
        
        # Assumes everything goes just peachy.
        
        conn = httplib.HTTPSConnection(host)
        conn.request("GET", url)
        res = conn.getresponse()
        response_data = res.read()
        
        self.data = json.loads(response_data)
        self.steps = []
        
        try:
            self.steps = self.data["routes"][0]["legs"][0]["steps"]
        except:
            print "Google driving directions didn't load properly for some reason. For now, just try again."
        
        conn.close()
    
    def render(self, lonToX, latToY, pgraphics):
        s = pgraphics.createShape()
        s.beginShape()
        
        def vertex(location):
            x = lonToX(float(location['lng']))
            y = latToY(float(location['lat']))
            s.vertex(x, y)
        
        for step in self.steps:
            vertex(step['start_location'])
            vertex(step['end_location'])
        
        s.endShape(LINES)
        pgraphics.shape(s, 0, 0)
    
    def draw(self):
        pass