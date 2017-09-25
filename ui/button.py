from control import Control

class Button(Control):
    def __init__(self, controlId, onClick=None, title=None, size=None, position=None):
        self.onClick = onClick
        super(Button, self).__init__(controlId, title=title, size=size, position=position)

    def draw(self, graphics):
        if not self.visible:
            return
        
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
