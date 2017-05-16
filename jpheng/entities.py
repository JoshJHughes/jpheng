import numpy as np
import jpheng.shapes as shapes


class Entity:
    """Parent class for all objects which are rendered in-simulation.
    Stores a position, velocity, acceleration, mass, radius, shape, damping
    constant, gravitational constant, type, force accumulator, and variable
    to determine whether an entity is 'alive', i.e. whether it should be
    deleted.
    Variables:
        p: Position, 3D numpy array, [x,y,z]
        v: Velocity
        a: Acceleration
        inv_mass: Inverse mass
        r: Characteristic length of entity, e.g. radius or side length
        shape: Entity shape from jpheng.shapes
        damping: Damping constant, see step function for usage
        g: Acceleration due to gravity
        type: Entity type, string, e.g. "firework"
        alive: Boolean, False if entity should be deleted, True otherwise
        force_accum: Net force acting on entity
    Methods:
        draw: Draw the entity
        move: Move the entity by dp
        step: Advance the entity's p,v using a and time step dt, update a
            using force_accum
        add_force: Add a force to the accumulator
        clear_force: Clear all forces acting on particle except gravity
    """
    def __init__(self, p, v, a, inv_mass):
        # physics properties
        self.p = np.array(p, dtype=float)  # position, [x,y,z]
        self.v = np.array(v, dtype=float)  # velocity, [x,y,z]
        self.a = np.array(a, dtype=float)  # acceleration, [x,y,z]
        self.inv_mass = inv_mass  # inverse mass
        self.r = None  # radius (or characteristic size, e.g. side length)
        self.shape = None  # shape from the shape classes in jpheng.shapes
        self.damping = None  # damping constant, see step function
        self.g = None  # Acceleration due to gravity
        self.type = None  # entity type, stored as string
        self.alive = True  # false if the entity should be deleted,
        # true otherwise
        self.force_accum = np.zeros(3)  # stores net force acting on the entity

    def draw(self):
        """Draw the entity on screen."""
        self.shape.draw()

    def move(self, dp):
        """Move the entity by dp, dp is a 3D numpy array, [x,y,z]."""
        self.p += dp
        # update vertex list with new position
        self.shape.move(dp)

    def step(self, dt):
        """Calculate the new position, velocity and acceleration of the
        particle based on its acceleration.  Uses simple Euler integration
        method."""
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
        """Add a force to the entity's accumulator."""
        self.force_accum += force

    def clear_force(self):
        """Clear all forces from the accumulator, gravity always acts and is
        not cleared."""
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
    """Class defining a bullet."""
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
    """Class defining an artillery shell."""
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
    """Class defining a fireball."""
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
    """Class defining a laser bullet."""
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
    """Class defining a firework.  Intended for use with rules found in
    'fireworks_demo.py'"""
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
        """In addition to default entity step, reduce fuse by dt."""
        super(Firework, self).step(dt)
        self.fuse -= dt
