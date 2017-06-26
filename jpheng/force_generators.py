import numpy as np

class ForceGenerator:
    """Interface for generator used to add forces to one or more particles.
    Methods:
        update_force: Update the force accumulator in the physics component 
            based on a time step of 'duration'.
    """
    def update_force(self, physics, duration):
        pass

# Gravity is hardcoded into entity class, this is for testing purposes only
class GravityGenerator(ForceGenerator):
    """Generator for gravity.
    Variables:
        g: Acceleration due to gravity
    Methods:
        update_force: Update the force accumulator in the physics component 
            based on a time step of 'duration'.
    """
    def __init__(self, gravity):
        self.g = gravity
    def update_force(self, physics, duration):
        """Update force on entity after time step of 'duration'"""
        # objects with inv_mass = 0 are considered fixed in place
        if physics.inv_mass == 0:
            return
        physics.force_accum += self.g/physics.inv_mass

class ParticleSpring(ForceGenerator):
    """Generator for spring force, each end is attached to a physics 
    component.  The component the generator acts on should be passed to 
    update_force, the component at the other end of the spring should be given 
    when initialised.
    Variables:
        k: spring constant
        l0: natural length of the spring
        other_physics: physics component which is anchored at the other 
        end of the spring
    Methods:
        update_force: Update the force accumulator in the physics component 
            based on a time step of 'duration'.
    """
    def __init__(self, other_physics, k, l0):
        self.k = k
        self.l0 = l0
        self.other_physics = other_physics
    def update_force(self, physics, duration):
        if physics.inv_mass == 0:
            return
        d = physics.p - self.other_physics.p
        f = -self.k*(np.abs(np.linalg.norm(d))-self.l0)*d/np.linalg.norm(d)
        physics.force_accum += f

class AnchoredSpring(ForceGenerator):
    """Generator for spring force, one end is attached to a physics
    component, the other is attached to a fixed point in space.
        Variables:
            k: spring constant
            l0: natural length of the spring
            anchor: numpy array containing the anchor point of the spring
        Methods:
            update_force: Update the force accumulator in the physics component
                based on a time step of 'duration'.
        """
    def __init__(self, anchor, k, l0):
        self.anchor = np.array(anchor)
        self.k = k
        self.l0 = l0
    def update_force(self, physics, duration):
        if physics.inv_mass == 0:
            return
        d = physics.p - self.anchor
        f = -self.k*(np.abs(np.linalg.norm(d))-self.l0)*d/np.linalg.norm(d)
        physics.force_accum += f

class AnchoredBungee(ForceGenerator):
    """Generator for spring force, one end is attached to a physics
    component, the other is attached to a fixed point in space.  Bungees
    provide extensive spring force but no compressive spring force.
        Variables:
            k: spring constant
            l0: natural length of the bungee
            anchor: numpy array containing the anchor point of the bungee
        Methods:
            update_force: Update the force accumulator in the physics component
                based on a time step of 'duration'.
        """
    def __init__(self, anchor, k, l0):
        self.anchor = np.array(anchor)
        self.k = k
        self.l0 = l0
    def update_force(self, physics, duration):
        if physics.inv_mass == 0:
            return
        d = physics.p - self.anchor
        if np.abs(np.linalg.norm(d)) <= self.l0:
            return
        f = -self.k*(np.abs(np.linalg.norm(d))-self.l0)*d/np.linalg.norm(d)
        physics.force_accum += f

