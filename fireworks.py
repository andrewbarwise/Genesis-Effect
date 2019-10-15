import pyglet
from particle import *
from pyglet.gl import *

#-drawing-constants---------------------------------------------------------------
WIDTH, HEIGHT, WINDOW_FS = 800, 600, True
TARGET_FPS = 30
# more constants here

if WINDOW_FS:
    win = pyglet.window.Window(fullscreen=True)
    WIDTH, HEIGHT = 1920, 1080
else:
    win = pyglet.window.Window(WIDTH, HEIGHT)

#-simulation-constants------------------------------------------------------------
MAX_PARTICLES = 100000
DELTA_T = 1/TARGET_FPS
# more constants here

#-main-update-function------------------------------------------------------------
# spawn initial particle system
particleSystem = ParticleSystem([0.0, 0.0, 0.0], [1.0, 1.0, 1.0])

# main loop driving simulation (set on timer)
frameNum = 0

def mainLoop(dt):
    global particleSystem, frameNum
    # update particle system
    particleSystem.update()
    particles = []
    if particleSystem.isParentSystem:
        for sys in particleSystem.children:
            sys.update()
            particles += sys.children
    else:
        particles = particleSystem.children

    # update particles
    reversedIndices = reversed(list(range(len(particles))))
    for ii in reversedIndices:
        particles[ii].update()
        if not particles[ii].alive: del particles[ii] # may be more efficient with numpy array

    # draw pixels -> may be able to remove one loop with reordering and optimisation
    glBegin(GL_POINTS)
    for pp in particles:
        glColor4f(pp.col[0], pp.col[1], pp.col[2], 1.0)
        glVertex3f(pp.pos[0], pp.pos[1], pp.pos[2])
    glEnd()

    frameNum += 1
    # frame.saveFrame(frameNum)? for making smooth video later
    print( "Frame %3d: %6d particles, %4d ms (%2d FPS)" % (frameNum, len(particles), dt, 1/dt) )
    return None

#-run-simluation------------------------------------------------------------------
pyglet.clock.schedule_interval(mainLoop, 1/TARGET_FPS)
pyglet.app.run()
