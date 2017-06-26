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

class StiffAnchoredSpring(ForceGenerator):
    """Generator for spring force, one end is attached to a physics
    component, the other is attached to a fixed point in space.  Natural
    length of the spring is 0. The method of simulation allows for stiffer
    spring constants without numerical instability but comes at the cost of
    sacrificing the ability to have a non-zero rest length and does not
    return the correct velocities.

    The force is calculated by calculating the target position of the
    physics component, p, and inverting the equation for p found in the
    physics update method to give
    p'' = 2*(p-p0)/(dt)^2 - 2*v/(dt)

    Solving the differential equation p'' = -k*p - d*p' gives
    p = [p0*cos(y*t) + c*sin(y*t)]*e^(-0.5d*t)
    with
    y = 0.5*sqrt(4k - d^2)
    c = p0*d/(2y) + p0'/y

    p is the position of the physics component relative to the anchor.  If
    the frequency of oscillation is imaginary the function simply returns
    with no effect.
    Variables:
        k: spring constant
        d: damping constant
        anchor: numpy array containing the anchor point of the spring
    Methods:
        update_force: Update the force accumulator in the physics component
        based on a time step of 'duration'.
    """
    def __init__(self, anchor, k, d=0.1):
        self.anchor= anchor
        self.k = k
        self.d = d
    def update_force(self, physics, duration):
        # check for infinite-mass
        if physics.inv_mass == 0: return

        # calculate constants
        freq2 = self.k - 0.25*self.d*self.d
        # check for critically/over-damped oscillation
        if freq2 <= 0: return
        gamma = 0.5*np.sqrt(freq2)
        p0 = physics.p - self.anchor
        c = (p0*self.d/(2*gamma)) + physics.v/gamma

        # calculate target position
        p = (p0*np.cos(gamma*duration) + c*np.sin(gamma*duration))*np.exp(
            -0.5*self.d*duration)

        # calculate acceleration
        a = 2*(p-p0)/(duration*duration) - 2*physics.v/duration
        physics.force_accum += a/physics.inv_mass

