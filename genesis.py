import math, random

import pyglet
from pyglet.gl import *
from genparts import *

#-drawing-constants---------------------------------------------------------------
WIDTH, HEIGHT, WINDOW_FS = 800, 600, True
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

#-sphere-drawing------------------------------------------------------------------
pos = [0, 0, -60]
rot_deg = 0
rot_vx, rot_vy, rot_vz = 0.0, 1.0, 0.0

def midpoint3f(p1, p2):
    return [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2]

MAX_DEPTH = 4
def subdivide(p1, p2, p3, depth=0):
    if depth == MAX_DEPTH:
        return p1+p2+p3
    else:
        p12, p13, p23 = midpoint3f(p1, p2), midpoint3f(p1, p3), midpoint3f(p2, p3)
        return subdivide(p1, p13, p12, depth+1) + subdivide(p12, p13, p23, depth+1) + subdivide(p12, p23, p2, depth+1) + subdivide(p13, p3, p23, depth+1)

r = 25.0
a = [0.0, 0.0, r]
b = [r, 0.0, 0.0]
c = [0.0, r, 0.0]

px, nx = [r, 0.0, 0.0], [-r, 0.0, 0.0]
py, ny = [0.0, r, 0.0], [0.0, -r, 0.0]
pz, nz = [0.0, 0.0, r], [0.0, 0.0, -r]

points =  subdivide(py, px, pz)
points += subdivide(py, px, nz)
points += subdivide(py, nx, pz)
points += subdivide(py, nx, nz)
points += subdivide(ny, px, pz)
points += subdivide(ny, px, nz)
points += subdivide(ny, nx, pz)
points += subdivide(ny, nx, nz)

alsoPoints = []
for i in range(0, len(points), 3):
    mag = math.sqrt(points[i]**2 + points[i+1]**2 + points[i+2]**2)
    points[i]   = r*points[i]/mag
    points[i+1] = r*points[i+1]/mag
    points[i+2] = r*points[i+2]/mag


#-main-update-function------------------------------------------------------------
# spawn initial particle system
systems = []

# main loop driving simulation (set on timer)
frameNum = 0

def mainLoop(dt):
    global pos_z, rot_deg, points

    win.clear()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, WIDTH/HEIGHT, 0.1, 50)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(*pos)
    glRotatef(rot_deg, rot_vx, rot_vy, rot_vz)

    # glBegin(GL_POINTS)
    # glColor4f(1.0, 1.0, 1.0, 0.8)
    # for i in range(0, len(points), 3):
    #     glVertex3f(points[i], points[i+1], points[i+2])
    # glEnd()

    glBegin(GL_TRIANGLES)
    glColor4f(1.0, 1.0, 1.0, 0.05)
    for i in range(0, len(points), 3):
        glVertex3f(points[i], points[i+1], points[i+2])
    glEnd()
    rot_deg += 0.2

    # particles
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
    glBegin(GL_POINTS)
    for pp in particles:
        if not pp.alive: print("This is not good")
        glColor4f(pp.col[0], pp.col[1], pp.col[2], pp.col[3])
        glVertex3f(pp.pos[0], pp.pos[1], pp.pos[2])
        # print(pp.pos[0], pp.pos[1], pp.pos[2])
    glEnd()

    frameNum += 1
    # frame.saveFrame(frameNum)? for making smooth video later
    print( "Frame %3d: %6d particles, %3d systems, %4d ms (%2d FPS)" % (frameNum, len(particles), len(systems), dt, 1/dt) )
    glFlush()

#-run-simluation------------------------------------------------------------------
def spawnParticle(t):
    global r
    # spherical coordinates
    polar, azimuth = random.random()*math.pi*2, random.random()*math.pi*2
    systems.append( ParticleSystem([r, polar, azimuth], [1.0, 0.5, 0.05, 0.95], [1.0, 0.0, 0.1, 0.5]) )

pyglet.clock.schedule_interval(mainLoop, 1/TARGET_FPS)
pyglet.clock.schedule_interval(spawnParticle, 0.5)
pyglet.app.run()
