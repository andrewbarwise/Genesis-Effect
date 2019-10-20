#-class-definitions---------------------------------------------------------------
class ParticleSystem:
    def __init__(self, position, color, parentSystem=False):
        # define system properties
        self.pos = [position[0], position[1], position[2]]
        self.col = [color[0], color[1], color[2]]
        self.children = []
        self.canSpawn = False
        self.alive = True
        # self.spawnType = particles (vs. nested particle systems)?
        # self.spawnCondition?
        return None

    def update(self):
        # move?
        # check life/spawning conditions
        # spawn new particles etc.
        return None

class Particle:
    def __init__(self, position, velocity, acceleration, color):
        # define particle properties
        self.pos = position
        self.vel = velocity
        self.acc = acceleration

        self.col = color
        self.age = 0
        self.alive = True
        # other properties
        return None

    def update(self):
        # physics calculations
        # visual changes (color etc.)
        # check for events (dying, spawning new particles etc.)

        # kill particle if off screen
        if self.pos[1] < 0: self.alive = False
        return None

#-helper/utility-functions--------------------------------------------------------
# COLOR INTERPOLATION
#   interpolated between the intial and final colors as RGB(A?)
#   age is the current age of the particle in frames
#   particle lifespan as the dying age of the particle in frames
#   (lifespan could be optional (=1) if age is a fraction 0.0->1.0)
def colorInterp(initial, final, age, particleLifespan = 1):
    frac = age/particleLifespan
    newR = intial[0] + frac*(final[0]-initial[0])
    newG = intial[1] + frac*(final[1]-initial[1])
    newB = intial[2] + frac*(final[2]-initial[2])
    return [newR, newG, newB]
