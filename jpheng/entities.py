import numpy as np
import jpheng.shapes as shapes


class Entity:
    def __init__(self, p, v, a, inv_mass):
        # physics properties
        self.p = np.array(p, dtype=float)  # position
        self.v = np.array(v, dtype=float)  # velocity
        self.a = np.array(a, dtype=float)  # acceleration
        self.inv_mass = inv_mass  # inverse mass
        self.r = None
        self.shape = None
        self.damping = None
        self.g = None
        self.type = None
        self.alive = True
        self.force_accum = np.zeros(3)

    def draw(self):
        self.shape.draw()

    def move(self, dp):
        self.p += dp
        # update vertex list with new position
        self.shape.move(dp)

    def step(self, dt):
        """Calculate the new position, velocity and acceleration of the
        particle based on its acceleration.  Uses simple Euler integration
        method.
        """
        # update position based on last step's velocity and acceleration
        dp = self.v*dt + 0.5*self.a*dt**2
        self.move(dp)
        # update velocity based on last step's acceleration, reduce previous
        # step's velocity by damping**dt to avoid numerical instability
        self.v = self.v*(self.damping**dt) + self.a*dt
        # set current acceleration by N2L
        self.a = self.force_accum*self.inv_mass
        # clear force accumulator
        self.clear_force()

    def add_force(self, force):
        self.force_accum += force

    def clear_force(self):
        self.force_accum = self.g/self.inv_mass


class Particle(Entity):
    """Class defining a point mass."""
    def __init__(self, p, v, a, inv_mass, r, color=None):
        Entity.__init__(self, p, v, a, inv_mass)
        self.r = r  # radius
        self.shape = shapes.Sphere(r, p, color=color)
        # Fraction of velocity retained each second, required to remove energy
        # added through numerical instability of the integrator.
        self.damping = 0.995
        # Gravity
        self.g = np.array([0, 0, 0])
        self.type = "particle"


class Bullet(Entity):
    def __init__(self, p, direction):
        v = 35*np.array(direction)
        a = np.zeros(3)
        inv_mass = 1/2
        Entity.__init__(self, p, v, a, inv_mass)
        self.r = 1
        self.shape = shapes.Sphere(self.r, p, color=(102,51,0))
        self.damping = 0.995
        self.g = np.array([0, 0, -1])
        self.type = "bullet"


class ArtilleryShell(Entity):
    def __init__(self, p, direction):
        v = 50*np.array(direction)
        a = np.zeros(3)
        inv_mass = 1/200
        Entity.__init__(self, p, v, a, inv_mass)
        self.r = 2
        self.shape = shapes.Sphere(self.r, p, color=(102,51,0))
        self.damping = 0.99
        self.g = np.array([0, 0, -20])
        self.type = "artillery_shell"


class Fireball(Entity):
    def __init__(self, p, direction):
        v = 10*np.array(direction)
        a = np.zeros(3)
        inv_mass = 1
        Entity.__init__(self, p, v, a, inv_mass)
        self.r = 4
        self.shape = shapes.Sphere(self.r, p, color=(255,0,0))
        self.damping = 0.9
        self.g = np.array([0, 0, 0.6])
        self.type = "fireball"


class Laser(Entity):
    def __init__(self, p, direction):
        v = 100*np.array(direction)
        a = np.zeros(3)
        inv_mass = 1/0.1
        Entity.__init__(self, p, v, a, inv_mass)
        self.r = 1
        self.shape = shapes.Sphere(self.r, p, color=(255,0,255))
        self.damping = 0.995
        self.g = np.array([0, 0, 0])
        self.type = "laser"


class Firework(Entity):
    def __init__(self, p, v, fuse, parent=False, generation=0):
        a = 0
        inv_mass = 1/200
        Entity.__init__(self, p, v, a, inv_mass)
        self.parent = parent
        self.r = 1
        self.damping = 0.995
        self.g = np.array([0, 0, -20])
        self.fuse = fuse
        self.type = "firework"
        self.generation = generation
        if self.generation > 1:
            self.parent = False
        if self.parent:
            self.shape = shapes.Sphere(self.r, p, color=(255,0,0))
        else:
            self.shape = shapes.Sphere(self.r, p, color=(0, 0, 255))

    def step(self, dt):
        super(Firework, self).step(dt)
        self.fuse -= dt
