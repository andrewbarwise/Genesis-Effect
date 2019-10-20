import pyglet
from pyglet.gl import *
import numpy as np
import math

pos = [0, 0, -60]
rot_deg = 0
rot_vx, rot_vy, rot_vz = 0.0, 1.0, 0.0

config = Config(sample_buffers=1, samples=8)
win = pyglet.window.Window(fullscreen=True, config=config)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

#-------------------------------------------------------------------------------
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

print(str(len(points)) + " vertices")
#-------------------------------------------------------------------------------
# https://stackoverflow.com/questions/54188353/how-do-i-make-3d-in-pyglet
def on_draw(t):

    global pos_z, rot_deg, points

    win.clear()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1920/1080, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(*pos)
    glRotatef(rot_deg, rot_vx, rot_vy, rot_vz)

    glBegin(GL_POINTS)
    glColor4f(1.0, 1.0, 1.0, 0.8)
    for i in range(0, len(points), 3):
        glVertex3f(points[i], points[i+1], points[i+2])
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor4f(1.0, 1.0, 1.0, 0.1)
    for i in range(0, len(points), 3):
        glVertex3f(points[i], points[i+1], points[i+2])
    glEnd()

    glFlush()
    rot_deg += 0.1

pyglet.clock.schedule_interval(on_draw, 1/60)
pyglet.app.run()
