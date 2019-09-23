import pyglet

#-drawing-constants---------------------------------------------------------------
WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_FS = , ,
TARGET_FPS =
# more constants here

#-simulation-constants------------------------------------------------------------
MAX_PARTICLES =
DELTA_T =
# more constants here

#-helper/utility-functions--------------------------------------------------------

# COLOR INTERPOLATION
#   interpolated between the intial and final colors as RGB(A?)
#   age is the current age of the particle in frames
#   particle lifespan as the dying age of the particle in frames
#   (lifespan could be optional (=1) if age is a fraction 0.0->1.0)
def colorInterp(initialColor, finalColor, age, particleLifespan):

    return newR, newG, newB, (newA?)

#-class-definitions---------------------------------------------------------------
class ParticleSystem:
    def __init__(self, someParameters):
        # define system properties
        # self.pos = [x, y, z]
        # self.col = [r, g, b, (a?)]
        # self.particles = []
        # self.canSpawn = False
        # self.spawnType = particles (vs. nested particle systems)?
        # self.spawnCondition?
        return None

    def update(self):
        # move?
        # check life/spawning conditions
        # spawn new particles etc.
        return None

class Particle:
    def __init__(self, someParameters):
        # define particle properties
        # self.pos = [x, y, z]
        # self.col = [r, g, b, (a?)]
        # self.canDie = False
        # other properties
        return None

    def update(self):
        # physics calculations
        # visual changes (color etc.)
        # check for events (dying, spawning new particles etc.)
        return None

#-main-update-function------------------------------------------------------------
# spawn initial particle system
particleSystem = ParticleSystem(someArgs)

# main loop driving simulation (set on timer)
frameNum = 0

@window event
def mainLoop(dt):
    # update particle system
    global particleSystem, frameNum
    particleSystem.update()
    # update particles
    particles = particleSystem.particles
    for ii in reversedIndices:
        particles[ii].update()
        if particles[ii].canDie: particles.pop(ii) # may be more efficient with numpy array

    # draw pixels -> may be able to remove one loop with reordering and optimaisation
    points, colors = [], []
    for pp in particles:
        points += pp.pos
        colors += pp.col
    window.drawAllPoints(points, colors)
    frameNum += 1
    # frame.saveFrame(frameNum)? for making smooth video later
    print("Frame %3d: %6d particles, %4dms interval" % (frameNum, len(particles) dt) )
    return None

#-run-simluation------------------------------------------------------------------
setInterval(mainLoop, 1/TARGET_FPS)
