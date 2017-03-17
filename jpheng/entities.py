import numpy as np
import jpheng.shapes as shapes


class Particle:
    """Class defining a point mass."""
    def __init__(self, p, v, a, inv_mass, r, color=None):
        # physics properties
        self.p = np.array(p, dtype=float)  # position
        self.v = np.array(v, dtype=float)  # velocity
        self.a = np.array(a, dtype=float)  # acceleration
        self.inv_mass = inv_mass  # inverse mass
        self.r = r  # radius
        self.shape = shapes.Sphere(r, color=color)
        # Fraction of velocity retained each second, required to remove energy
        # added through numerical instability of the integrator.
        self.damping = 0.995
        # Gravity
        # self.g = np.array([0, -9.81, 0])
        self.g = np.zeros(3)

    def draw(self):
        self.shape.draw()

    def step(self, dt):
        """Calculate the new position, velocity and acceleration of the
        particle based on its acceleration.  Uses simple Euler integration
        method.
        """
        # update position based on last step's velocity and acceleration
        dp = self.v*dt + 0.5*self.a*dt**2
        self.p += dp
        # update velocity based on last step's acceleration, reduce previous
        # step's velocity by damping**dt to avoid numerical instability
        self.v = self.v*(self.damping**dt) + self.a*dt
        # set acceleration to current acceleration
        self.a = self.g
        # update vertex list with new position
        self.shape.move(dp)
