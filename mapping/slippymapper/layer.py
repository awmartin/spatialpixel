
def defaultrenderer(layer, underlay):
    pass

class SlippyLayer(object):
    '''Creates an arbitrary SlippyMapper layer, given a function that draws objects.'''

    def __init__(self, renderer=None):
        self.renderer = renderer if renderer is not None else defaultrenderer
        self.underlayMap = None

    def setUnderlayMap(self, m):
        self.underlayMap = m

    def render(self):
        self.layer = createGraphics(self.underlayMap.width, self.underlayMap.height)
        self.layer.beginDraw()
        self.renderer(self.layer, self.underlayMap)
        self.layer.endDraw()

    def draw(self):
        image(self.layer, 0, 0)
