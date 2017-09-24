from control import Control

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
