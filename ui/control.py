class Control(object):
    def __init__(self, controlId, title=None, size=None, position=None):
        self.controlId = controlId
        self.title = self.controlId if title is None else title
        self.size = (100, 20) if size is None else size
        self.position = (0, 0) if position is None else position
        self.controller = None

    @property
    def sketch(self):
        return self.controller.sketch
    @property
    def x(self):
        return self.position[0]
    @property
    def y(self):
        return self.position[1]
    @property
    def width(self):
        return self.size[0]
    @property
    def height(self):
        return self.size[1]
    @property
    def mouseHover(self):
        isBetweenX = self.x < self.sketch.mouseX and self.sketch.mouseX < self.x + self.width
        isBetweenY = self.y < self.sketch.mouseY and self.sketch.mouseY < self.y + self.height
        return isBetweenX and isBetweenY

    def click(self):
        pass
