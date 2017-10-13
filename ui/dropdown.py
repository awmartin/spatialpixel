from control import Control
import button

class DropDown(Control):
    def __init__(self, controlId, options, getter, setter, title=None, size=None, position=None):
        self.options = options
        self.getter = getter
        self.setter = setter

        self.state = 'closed'

        super(DropDown, self).__init__(controlId, title=title, size=size, position=position)

        self.optionButtons = []

    def setController(self, controller):
        super(DropDown, self).setController(controller)
        self.buildOptions()

    def buildOptions(self):
        pos = self.height + self.y

        for key in self.options:
            opt = button.Button(
                self.controlId + key,
                title=key,
                onClick=self.getClick(key),
                size=self.size,
                position=(self.x, pos)
                )
            opt.hide()
            self.optionButtons.append(opt)
            self.controller.addControl(opt)

            pos += self.height

    def getClick(self, key):
        def optionClick():
            self.setter(key)
            self.close()
        return optionClick

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

        title = self.getter().upper()
        graphics.text(title, self.x + 5, self.y + 15)

        for opt in self.optionButtons:
            opt.draw(graphics)

    def click(self):
        if self.mouseHover:
            if self.state == 'open':
                self.close()
            elif self.state == 'closed':
                self.open()

    def open(self):
        self.state = 'open'
        for opt in self.optionButtons:
            opt.show()

    def close(self):
        self.state = 'closed'
        self.controller.clear()
        for opt in self.optionButtons:
            opt.hide()
