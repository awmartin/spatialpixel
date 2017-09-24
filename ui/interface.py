class Interface(object):
    def __init__(self, sketch, fontName=None):
        self.sketch = sketch
        self.font = self.sketch.loadFont(fontName) if fontName is not None else None

        self.controls = {}
        self.graphics = self.sketch.createGraphics(self.sketch.width, self.sketch.height)

    def addControl(self, control):
        self.controls[control.controlId] = control
        control.controller = self

    def draw(self, mousePressed):
        self.mousePressed = mousePressed
        self.graphics.beginDraw()
        if self.font is not None:
            self.graphics.textFont(self.font, 12)
        for control in self.controls.values():
            control.draw(self.graphics)
        self.graphics.endDraw()
        self.sketch.image(self.graphics, 0, 0)

    def click(self):
        for control in self.controls.values():
            control.click()

    def getControl(self, controlId):
        return self.controls[controlId]
