import numpy as np

class PhysicsComponent:
    """Class which contains physics state and methods to describe,
    manipulate, and update an abstract physics object.
    Variables:
        p: Position, 3D numpy float array, [x,y,z]
        v: Velocity, 3D numpy float array, [x,y,z]
        a: Acceleration, 3D numpy float array, [x,y,z]
        inv_mass: Inverse mass, float
        damping: Damping constant, float, see step function for usage
        g: Acceleration due to gravity, float
        force_accum: Net force acting on component, float
        force_registry: list containing ForceGenerators which define the forces
            acting on the component
    """
    def __init__(self, p, v, a, inv_mass, g = np.array([0,0,-20]),
                 damping = 0.999):
        # set physical properties of component
        self.p = np.array(p, dtype=float)  # position, numpy array, [x,y,z]
        self.v = np.array(v, dtype=float)  # velocity, numpy array, [x,y,z]
        self.a = np.array(a, dtype=float)  # acceleration, numpy array, [x,y,z]
        self.inv_mass = inv_mass  # inverse mass, float
        self.g = np.array(g, dtype=float)  # accel. due to gravity, [x,y,z]
        self.damping = damping  # damping constant, float, see step function
        # store values relating to forces
        self.force_accum = np.zeros(3)  # stores net force acting on the
                                        # component
        self.force_registry = []

    def clear_force_accumulator(self):
        """Clear all forces from the accumulator, gravity always acts and is
        not cleared."""
        self.force_accum = self.g/self.inv_mass

    def add_generator(self, generator):
        """Add additional force generator to the component's registry."""
        self.force_registry.append(generator)

    def remove_generator(self, generator):
        """Remove force generator from the component's registry."""
        self.force_registry.remove(generator)

    def update(self, dt):
        """Calculate the new position, velocity and acceleration of the
        particle based on its acceleration.  Uses simple Euler integration
        method."""
        # update all forces using time step dt
        for generator in self.force_registry:
            generator.update_force(self, dt)
        # update position based on last step's velocity and acceleration
        self.p += self.v*dt + 0.5*self.a*dt**2
        # update velocity based on last step's acceleration, reduce previous
        # step's velocity by damping**dt to avoid numerical instability
        self.v = self.v*(self.damping**dt) + self.a*dt
        # set current acceleration by N2L
        self.a = self.force_accum*self.inv_mass
        # clear force accumulator
        self.clear_force_accumulator()
