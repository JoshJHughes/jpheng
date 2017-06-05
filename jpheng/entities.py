import numpy as np
import jpheng.physics as phy
import jpheng.graphics as gra


class Entity:
    """Parent class for all objects which are rendered in-simulation.
    Stores a position, velocity, acceleration, mass, radius, shape, damping
    constant, gravitational constant, type, force accumulator, and variable
    to determine whether an entity is 'alive', i.e. whether it should be
    deleted.
    Variables:
        physics: PhysicsComponent object, handles entity physics
        graphics: GraphicsComponent object, handles entity graphics

        type: Entity type, string, e.g. "firework"
        alive: Boolean, False if entity should be deleted, True otherwise
    Methods:
        draw: Draw the entity
        update: Call the component update routines
    """
    def __init__(self, physics, graphics):
        self.physics = physics
        self.graphics = graphics

    def draw(self):
        """Draw the entity on screen."""
        self.graphics.draw()

    def update(self, dt):
        """Call the component update routines."""
        self.physics.update(dt)
        self.graphics.update(self, dt)


class Particle(Entity):
    """Class defining a point mass."""
    def __init__(self, p, v, a, inv_mass, r, color=None):
        physics = phy.PhysicsComponent(p, v, a, inv_mass)
        graphics = gra.SphereComponent(r, color)
        Entity.__init__(self, physics, graphics)


class Laser(Entity):
    """Class defining a laser bullet."""
    def __init__(self, p, direction):
        v = 100*np.array(direction)
        a = np.zeros(3)
        inv_mass = 1/0.1
        color = (255, 0, 255)
        r = 1
        g = np.array([0,0,0])
        physics = phy.PhysicsComponent(p, v, a, inv_mass, g)
        graphics = gra.SphereComponent(r, color)
        Entity.__init__(self, physics, graphics)


class Firework(Entity):
    """Class defining a firework.  Intended for use with rules found in
    'fireworks_demo.py'"""
    def __init__(self, p, v, fuse, parent=True, generation=0):
        a = [0,0,0]
        inv_mass = 1/200
        r = 1
        self.fuse = fuse
        self.generation = generation

        if self.generation > 1:
            parent = False
        self.parent = parent

        if self.parent:
            color=(255,0,0)
        else:
            color=(0, 0, 255)

        physics = phy.PhysicsComponent(p, v, a, inv_mass)
        graphics = gra.SphereComponent(r, color)
        Entity.__init__(self, physics, graphics)

    def update(self, dt):
        """In addition to default entity update, reduce fuse by dt."""
        Entity.update(self, dt)
        self.fuse -= dt
