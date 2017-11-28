"""Dropdown controls for spatialpixel.ui.

Arguments:

- controlId - an arbitrary string to uniquely identify the control
- options - a dict or list of options, or a function that returns such a list or dict
- getter - a function that will return the currently selected option
- setter - a function called when a user selects an option, takes one argument
- title - the default displayed title as a string
- size - a tuple of (width, height) in pixels
- position - a tuple of (x, y) in pixels of the upper-left corner of the control
"""

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
