import math, random

import pyglet
from pyglet.gl import *
from particle import *

#-drawing-constants---------------------------------------------------------------
WIDTH, HEIGHT, WINDOW_FS = 800, 600, False
TARGET_FPS = 24
# more constants here

if WINDOW_FS:
    win = pyglet.window.Window(fullscreen=True)
    WIDTH, HEIGHT = 1920, 1080
else:
    win = pyglet.window.Window(WIDTH, HEIGHT)

# enable transparency
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

#-simulation-constants------------------------------------------------------------
MAX_PARTICLES = 100000
DELTA_T = 1/TARGET_FPS
# more constants here

#-main-update-function------------------------------------------------------------
# spawn initial particle system
systems = []

# main loop driving simulation (set on timer)
frameNum = 0

def mainLoop(dt):
    global systems, frameNum
    # update particle system
    particles = []
    for index, sys in reversed(list(enumerate(systems))):
        sys.update(DELTA_T)
        if sys.alive:
            particles += sys.children
        else:
            del systems[index]
    # particles updated by parents

    # draw pixels -> may be able to remove one loop with reordering and optimisation
    win.clear()
    glBegin(GL_POINTS)
    for pp in particles:
        glColor4f(pp.col[0], pp.col[1], pp.col[2], pp.col[3])
        glVertex3f(pp.pos[0], pp.pos[1], pp.pos[2])
        # print(pp.pos[0], pp.pos[1], pp.pos[2])
    glEnd()

    frameNum += 1
    # frame.saveFrame(frameNum)? for making smooth video later
    print( "Frame %3d: %6d particles, %3d systems, %4d ms (%2d FPS)" % (frameNum, len(particles), len(systems), dt, 1/dt) )
    return None

#-run-simluation------------------------------------------------------------------
def spawnParticle(t):
    xpos = random.uniform(0, WIDTH/2)
    systems.append( ParticleSystem([xpos, HEIGHT/2, 0], [1.0, 0.0, 0.0, 0.8], [0.0, 1.0, 0.0, 0.1]) )

pyglet.clock.schedule_interval(mainLoop, 1/TARGET_FPS)
pyglet.clock.schedule_interval(spawnParticle, 0.1)
pyglet.app.run()
