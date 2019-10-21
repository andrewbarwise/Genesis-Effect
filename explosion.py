import math, random

import numpy as np

import pyglet
from pyglet.gl import *
from genparts  import *

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
pos = [0, 0, -100]
rot_deg = 60
rot_vx, rot_vy, rot_vz = 0.0, 1.0, 0.1

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
    gluPerspective(90, WIDTH/HEIGHT, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(*pos)
    # glRotatef(rot_deg, rot_vx, rot_vy, rot_vz)
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
    rot_deg -= 0

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
        glColor4f(pp.col[0], pp.col[1], pp.col[2], pp.col[3])
        glVertex3f(pp.pos[0], pp.pos[1], pp.pos[2])
        # print(pp.pos[0], pp.pos[1], pp.pos[2])
    glEnd()

    frameNum += 1
    # pyglet.image.get_buffer_manager().get_color_buffer().save('splosion/' + str(frameNum)+'.png')
    print( "Frame %3d: %6d particles, %3d systems, %4d ms (%2d FPS)" % (frameNum, len(particles), len(systems), dt, 1/dt) )
    glFlush()

#-run-simluation------------------------------------------------------------------
iteration = 0
# diameter = np.linspace(-r, r, 100)
# DENSITY = 0.9
diameter = np.linspace(-r, -r+0.25, 20)
DENSITY = 1
LIFE_MEAN, LIFE_VAR = 2, 1

def spawnParticle(t):
    global r, iteration

    if 4<iteration < 10:
        for ii in range(2):
            systems.append( ParticleSystem([-r, 0, 0], [1.0, 0.75, 0.01, 1.0], [1.0, 0.5, 0.1, 0.3], lifespan=2*LIFE_MEAN, speed=80, var=20, spawnrad=0.01) )

    if 6<iteration < 20:
        # spherical coordinates
        x = diameter[iteration]
        minRad = math.sqrt( r**2 - x**2 )
        # print(iteration, x, minorRadius)
        for ii in range(round(DENSITY*minRad)):
            ang = random.uniform(0, 2*math.pi)
            life = LIFE_MEAN + random.uniform(-LIFE_VAR, LIFE_VAR)
            systems.append( ParticleSystem([x, minRad*math.sin(ang), minRad*math.cos(ang)], [1.0, 0.65, 0.05, 0.75], [1.0, 0.0, 0.1, 0.1], lifespan=life, spawnrad=0.05) )

        # systems.append( ParticleSystem([25, 0, 0], [1.0, 0.5, 0.05, 0.95], [1.0, 0.0, 0.1, 0.5]) )
        # systems.append( ParticleSystem([0, 25, 0], [0.0, 1.0, 0.05, 0.95], [0.0, 1.0, 0.1, 0.5]) )
        # systems.append( ParticleSystem([0, 0, 25], [0.0, 0.5, 1.00, 0.95], [0.0, 0.0, 1.0, 0.5]) )
        # systems.append( ParticleSystem([-25, 0, 0], [1.0, 0.5, 0.05, 0.95], [1.0, 0.0, 0.1, 0.5]) )
        # systems.append( ParticleSystem([0, -25, 0], [0.0, 1.0, 0.05, 0.95], [0.0, 1.0, 0.1, 0.5]) )
        # systems.append( ParticleSystem([0, 0, -25], [0.0, 0.5, 1.00, 0.95], [0.0, 0.0, 1.0, 0.5]) )
    iteration = (iteration+1)%200


pyglet.clock.schedule_interval(mainLoop, 1/TARGET_FPS)
pyglet.clock.schedule_interval(spawnParticle, 0.25)
pyglet.app.run()
