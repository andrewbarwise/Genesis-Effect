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

def spawnParticle(t):
    print(t)

#-main-update-function------------------------------------------------------------
# spawn initial particle system
systems = [ParticleSystem([0.0, 0.0, 0.0], [1.0, 1.0, 1.0])]

# main loop driving simulation (set on timer)
frameNum = 0

def mainLoop(dt):
    global systems, frameNum
    # update particle system
    particles = []
    for sys in systems:
        sys.update()
        particles += sys.children

    # update particles
    for sys, index in reversed(list(enumerate(systems))):
        sys.update()
        if sys.alive:
            particles += sys.children
        else:
            del systems[index]


    # update particles
    for particle, index in reversed(list(enumerate(particles))):
        particle.update()
        if not particle.alive: del particles[index] # may be more efficient with numpy array

    # draw pixels -> may be able to remove one loop with reordering and optimisation
    glBegin(GL_POINTS)
    for pp in particles:
        glColor4f(pp.col[0], pp.col[1], pp.col[2], 0.9)
        glVertex3f(pp.pos[0], pp.pos[1], pp.pos[2])
    glEnd()

    frameNum += 1
    # frame.saveFrame(frameNum)? for making smooth video later
    print( "Frame %3d: %6d particles, %4d ms (%2d FPS)" % (frameNum, len(particles), dt, 1/dt) )
    return None

#-run-simluation------------------------------------------------------------------
pyglet.clock.schedule_interval(mainLoop, 1/TARGET_FPS)
pyglet.clock.schedule_interval(spawnParticle, 1.0)
pyglet.app.run()
