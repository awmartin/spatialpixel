# add_library('peasycam')
import randomwalkgenerator as rwg
import procgui


def setup():
    size(1000, 800, P2D)
    
    global panX, panY
    panX = 0
    panY = 0
    
    global gui
    gui = procgui.ProcGui(this)
    gui.addControl(procgui.Button("reset", onClick=reset, title="Reset", size=(100, 20), position=(20, 20)))
    gui.addControl(procgui.Toggle("overlap", onToggle=toggleOverlap, title="Overlap", size=(100, 20), position=(140, 20)))
    gui.addControl(procgui.Text("info", value=lambda: len(walker.path), title="Steps", position=(260, 20)))
    
    # global cam
    # cam = PeasyCam(this, 100)
    # cam.setMinimumDistance(50)
    # cam.setMaximumDistance(500)
    
    global render
    render = createGraphics(width, height)
    
    global walker
    walker = rwg.RandomWalkGenerator(is3D=False, allowOverlap=True)
    
    # To run the path and draw it as it searches, call the start() method and
    # in draw(), use the step() method to draw the path.
    walker.start((0, 0), 1000)
    
    # To run the entire generate loop and just get the final path (much faster),
    # call the generate() method and draw the path immediately.
    # walker.generate((0, 0), 10000)
    
    # For each step, how many pixels to move.
    global step
    step = 5.0
    
    background(255)

def draw():
    walker.step()
    walker.resetIfNecessary()
    
    pushMatrix()
    background(255)
    translate(panX, panY)
    # drawPath(walker.path)
    drawLastStep(walker.path)
    popMatrix()
    
    gui.draw(mousePressed)

def keyPressed():
    if key in (' ', 'r'):
        reset()

def reset():
    walker.start((0, 0), 1000)
    # walker.generate((0, 0), 10000)

def toggleOverlap():
    walker.allowOverlap = gui.getControl('overlap').value

def mouseDragged():
    global panX, panY
    panX += (mouseX - pmouseX)
    panY += (mouseY - pmouseY)

def mouseClicked():
    gui.click()

def drawLastStep(path):
    if len(path) < 2:
        return
    
    a = path[-1]
    b = path[-2]
    
    render.beginDraw()
    render.stroke(0, 192)
    render.noFill()
    render.translate(render.width / 2, render.height / 2)
    render.line(a[0] * step, a[1] * step, b[0] * step, b[1] * step)
    render.endDraw()
    
    image(render, 0, 0)
    
    drawAgent(path[-1])

def drawPath(path):
    stroke(0)
    noFill()
    s = createShape()
    s.beginShape()
    
    for location in path:
        x = location[0] * step
        y = location[1] * step
        # z = location[2] * step
        s.vertex(x, y)
    
    s.endShape()
    translate(width / 2, height / 2)
    shape(s)
    
    drawAgent(path[-1])
    
def drawAgent(location):
    # Draw the agent.
    fill(255, 0, 0)
    noStroke()
    
    # For drawPath()
    # translate(location[0] * step, location[1] * step)
    
    # For drawLastStep()
    translate(location[0] * step + render.width / 2, location[1] * step + render.height / 2)
    
    # 3D
    # translate(location[0] * step, location[1] * step, location[2] * step)
    
    ellipse(0, 0, 5, 5)