import numpy as np
import jpheng.physics as phy
import jpheng.graphics as gra


class Particle:
    """Parent class for all particle objects which are rendered in-simulation.
    Stores a PhysicsComponent and a GraphicsComponent, the former of which
    describes the particle's physics properties and behaviour, the latter of
    which describes the graphical properties and drawing methods.
    Variables:
        physics: PhysicsComponent object, handles entity physics
        graphics: GraphicsComponent object, handles entity graphics
    Methods:
        draw: Draw the particle
        step: Call the component step routines
    """
    def __init__(self, physics, graphics):
        self.physics = physics
        self.graphics = graphics

    def draw(self):
        """Draw the entity on screen."""
        self.graphics.draw()

    def step(self, dt):
        """Call the component update routines."""
        self.physics.step(dt)
        self.graphics.step(self, dt)


class QuickParticle(Particle):
    """Class defining a point mass."""
    def __init__(self, p, v, a, inv_mass, r, color=None):
        physics = phy.PhysicsComponent(p, v, a, inv_mass)
        graphics = gra.SphereComponent(r, color)
        Particle.__init__(self, physics, graphics)


class Laser(Particle):
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
        Particle.__init__(self, physics, graphics)


class Firework(Particle):
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
        Particle.__init__(self, physics, graphics)

    def step(self, dt):
        """In addition to default entity update, reduce fuse by dt."""
        Particle.step(self, dt)
        self.fuse -= dt
