"""Enables rendering OpenStreetMap data in a SlippyMapper map."""


def defaultStyler(feature, graphics):
    if feature['type'] == 'way':
        graphics.noFill()
        graphics.stroke(255, 0, 0)

    elif feature['type'] == 'node':
        # graphics.stroke(255)
        # graphics.fill(255)
        return False

    else:
        return False


class SlippyLayer(object):
    def __init__(self, osm, styler=None):
        self.source = osm
        self.styler = styler if styler is not None else defaultStyler
        
        self.underlayMap = None
    
    # TODO extend rendering to include relations, whatever those mean.

    @property
    def ways(self):
        return self.source.entities["ways"]
    
    @property
    def nodes(self):
        return self.source.entities["nodes"]

    def setUnderlayMap(self, m):
        self.underlayMap = m

    def render(self):
        self.layer = createGraphics(self.underlayMap.width, self.underlayMap.height)
        self.layer.beginDraw()
        self.renderLayer(self.underlayMap.lonToX, self.underlayMap.latToY, self.layer, self.styler)
        self.layer.endDraw()

    def draw(self):
        image(self.layer, 0, 0)

    def renderLayer(self, lonToX, latToY, pgraphics, styler=None):
        for wayid, way in self.ways.iteritems():
            should_draw = True

            if styler is not None:
                should_draw = styler(way, pgraphics)
                if should_draw is None:
                    should_draw = True

            if should_draw:
                s = pgraphics.createShape()
                s.beginShape()
                for nodeid in way['nodes']:
                    node = self.nodes[nodeid]
                    s.vertex(lonToX(node['lon']), latToY(node['lat']))
                s.endShape()
                pgraphics.shape(s, 0, 0)

        for nodeid, node in self.nodes.iteritems():
            should_draw = True

            if styler is not None:
                should_draw = styler(node, pgraphics)
                if should_draw is None:
                    should_draw = True
            
            if should_draw:
                x, y = lonToX(node['lon']), latToY(node['lat'])
                pgraphics.ellipse(x, y, 4, 4)
