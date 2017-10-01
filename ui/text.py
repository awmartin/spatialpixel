from control import Control

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
