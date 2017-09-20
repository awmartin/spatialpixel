class Panner(object):
    def __init__(self, sketch, x=0, y=0):
        self.sketch = sketch
        self.originalPanX = x
        self.originalPanY = y
        self.panX = x
        self.panY = y
        self.zoomFactor = 1.0
    
    def reset(self):
        self.panX = self.originalPanX
        self.panY = self.originalPanY
    
    def pan(self):
        self.sketch.translate(self.panX, self.panY)
        self.sketch.scale(self.zoomFactor)
        
        # Scaling affects the strokeWeight, so let's undo that so we're not rendering crap.
        self.sketch.strokeWeight(1.0 / self.zoomFactor)
    
    def drag(self):
        self.panX += (self.sketch.mouseX - self.sketch.pmouseX)
        self.panY += (self.sketch.mouseY - self.sketch.pmouseY)

    def zoom(self, event):
        origX, origY = self.sketch.width * self.zoomFactor, self.sketch.height * self.zoomFactor
        
        # Change the desired zoom value
        count = event.getCount()
        self.zoomFactor -= count / 100.0
        self.zoomFactor = max(self.zoomFactor, 0.01)
        
        # Adjust the pan of the map view to center around the center of the sketch window
        newX, newY = self.sketch.width * self.zoomFactor, self.sketch.height * self.zoomFactor
        self.panX += (origX - newX)
        self.panY += (origY - newY)