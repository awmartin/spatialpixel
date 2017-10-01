class ProcGui(object):
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


class Button(Control):
    def __init__(self, controlId, onClick=None, title=None, size=None, position=None):
        self.onClick = onClick
        super(Button, self).__init__(controlId, title=title, size=size, position=position)

    def draw(self, graphics):
        graphics.noStroke()
        if self.mouseHover:
            graphics.fill(0, 100, 150)
            if self.controller.mousePressed:
                graphics.fill(0, 150, 250)
        else:
            graphics.fill(0, 50, 100)
        graphics.rect(self.x, self.y, self.width, self.height)
        graphics.fill(255)
        graphics.text(self.title.upper(), self.x + 5, self.y + 15)

    def click(self):
        if self.mouseHover and self.onClick is not None:
            self.onClick()

class Toggle(Control):
    def __init__(self, controlId, onToggle=None, state=False, title=None, size=None, position=None):
        self.on = state
        self.onToggle = onToggle
        super(Toggle, self).__init__(controlId, title=title, size=size, position=position)
    
    def draw(self, graphics):
        graphics.noStroke()
        
        if self.mouseHover:
            if self.on:
                graphics.fill(150, 100, 0)
            else:
                graphics.fill(0, 100, 150)
            
            if self.controller.mousePressed:
                graphics.fill(0, 150, 250)
        else:
            if self.on:
                graphics.fill(100, 50, 0)
            else:
                graphics.fill(0, 50, 100)
        
        graphics.rect(self.x, self.y, self.width, self.height)
        
        graphics.fill(255)
        graphics.text(self.title.upper(), self.x + 5, self.y + 15)

    def click(self):
        if self.mouseHover:
            self.on = not self.on
            if self.onToggle is not None:
                self.onToggle()
    
    @property
    def value(self):
        return self.on


class Text(Control):
    def __init__(self, controlId, value=None, title=None, size=None, position=None):
        self.value = value
        super(Text, self).__init__(controlId, title=title, size=size, position=position)
    
    def draw(self, graphics):
        graphics.noStroke()
        
        graphics.fill(255)
        graphics.rect(self.x, self.y, self.width, self.height)
        
        graphics.fill(0, 50, 100)
        if self.value is not None:
            graphics.text(self.title.upper() + " " + str(self.value()), self.x + 5, self.y + 15)
        else:
            graphics.text(self.title.upper(), self.x + 5, self.y + 15)