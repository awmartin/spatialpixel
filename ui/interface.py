"""Build standard, boring user interfaces in processing.py.

An Interface object can hold multiple Controls that represent standard
UI elements, like buttons, dropdown menus, etc.

To create an interface:

    import spatialpixel.ui as ui

    def setup():
        global gui
        gui = ui.Interface(this)

    def draw():
        global gui
        gui.draw(mousePressed)

    def mouseClicked():
        global gui
        gui.click()
"""

class Interface(object):
    def __init__(self, sketch, fontName=None):
        self.sketch = sketch
        self.font = self.sketch.loadFont(fontName) if fontName is not None else None

        self.controls = {}
        self.graphics = self.sketch.createGraphics(self.sketch.width, self.sketch.height)

    def addControl(self, control):
        self.controls[control.controlId] = control
        control.setController(self)

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
            if control.isVisible:
                control.click()

    def getControl(self, controlId):
        """Returns a Control instance given its id."""

        if controlId in self.controls:
            return self.controls[controlId]
        return None

    def clear(self):
        self.graphics.beginDraw()
        self.graphics.background(self.graphics.color(0,0,0), 0)
        self.graphics.endDraw()
