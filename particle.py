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


# gravity, act as our constant g, you can experiment by changing it
GRAVITY = 0.05
# list of color, can choose randomly or use as a queue (FIFO)
colors = ['red', 'blue', 'yellow', 'white', 'green', 'orange', 'purple']

class Particle:
    def __init__(self, total, explosion_speed, xx=0., yy=0., vx = 0., vy = 0., size=2., color = 'red', lifespan = 2, **kwargs):
        # define particle properties    
        self.x = xx
        self.y = yy
        self.initial_speed = explosion_speed
        self.vx = vx
        self.vy = vy
        self.total = total
        self.age = 0
        self.color = color
        self.cid = self.cv.create_oval(
            xx - size, yy - size, xx + size,
            yy + size, fill=self.color)
        self.lifespan = lifespan


    def update(self, dt):
        self.age += dt

        # particle expansions
        if self.alive() and self.expand():
            move_x = cos(radians(self.id*360/self.total))*self.initial_speed
            move_y = sin(radians(self.id*360/self.total))*self.initial_speed
            self.cv.move(self.cid, move_x, move_y)
            self.vx = move_x/(float(dt)*1000)

        # falling down in projectile motion
        elif self.alive():
            move_x = cos(radians(self.id*360/self.total))
            # we technically don't need to update x, y because move will do the job
            self.cv.move(self.cid, self.vx + move_x, self.vy+GRAVITY*dt)
            self.vy += GRAVITY*dt

        # remove article if it is over the lifespan
        elif self.cid is not None:
            cv.delete(self.cid)
            self.cid = None

    # define time frame for expansion
    def expand (self):
        return self.age <= 1.2

    # check if particle is still alive in lifespan
    def alive(self):
        return self.age <= self.lifespan

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
