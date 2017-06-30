import numpy as np

class ParticleLink:
    """Connects two particles together, generating a contact if they violate
    the constraints of their link.
    Variables:
        particles: list of particles affected by the link
    Methods:
        current_length: Returns the current length of the link.
        fill_contact: Fills the given contact with the information necessary to
            keep the link from violating its constraint.
    """
    def __init__(self, particles):
        self.particles = particles

    def current_length(self):
        separation = self.particles[0].physics.p - self.particles[1].physics.p
        separation = np.linalg.norm(separation)
        return separation

    def fill_contact(self, contact):
        """Fills the given contact with the information necessary to keep
        the link from violating its constraint.
        """


class ParticleCable(ParticleLink):
    """Cables keep particles within a certain distance of each other.
    Variables:
        See parent class
        max_length: Maximum extension of the cable
        restitution: Restitution of contacts filled by this cable"""
    def __init__(self, particles, max_length, restitution):
        super(ParticleCable, self).__init__(particles)
        self.max_length = max_length
        self.restitution = restitution

    def fill_contact(self, contact):
        # get current length
        length = self.current_length()
        # check if cable is overextended
        if length < self.max_length:
            return False
        contact.particles[0] = self.particles[0]
        contact.particles[1] = self.particles[1]
        p_sep = self.particles[1].physics.p - self.particles[0].physics.p
        normal = p_sep/np.linalg.norm(p_sep)
        contact.normal = normal
        contact.penetration = length-self.max_length
        contact.restitution = self.restitution
        return True


class ParticleRod(ParticleLink):
    """Rods link a pair of particles, generating contacts if they stray too
    far or too close.
    Variables:
        length: Holds the length of the rod
    """
    def __init__(self, particles, length):
        super(ParticleRod, self).__init__(particles)
        self.length = length

    def fill_contact(self, contact):
        current_length = self.current_length()
        if current_length == self.length:
            return False
        contact.particles[0] = self.particles[0]
        contact.particles[1] = self.particles[1]
        p_sep = self.particles[1].physics.p - self.particles[0].physics.p
        normal = p_sep/np.linalg.norm(p_sep)
        if current_length > self.length:
            contact.normal = normal
            contact.penetration = current_length - self.length
        else:
            contact.normal = -1*normal
            contact.penetration = self.length - current_length
        contact.restitution = 0
        return True
