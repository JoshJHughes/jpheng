import numpy as np
import jpheng.pcontacts as pcontacts

class ParticleLink(pcontacts.ParticleContactGenerator):
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

    def gen_contacts(self):
        # get current length
        length = self.current_length()
        # check if cable is overextended
        if length < self.max_length:
            return []
        contact_pair = [self.particles[0], self.particles[1]]
        p_sep = self.particles[1].physics.p - self.particles[0].physics.p
        normal = p_sep/np.linalg.norm(p_sep)
        penetration = length - self.max_length
        contact = pcontacts.ParticleContact(contact_pair,
                                  self.restitution, normal, penetration)
        return [contact]


class ParticleRod(ParticleLink):
    """Rods link a pair of particles, generating contacts if they stray too
    far or too close.
    Variables:
        length: Holds the length of the rod
    """
    def __init__(self, particles, length):
        super(ParticleRod, self).__init__(particles)
        self.length = length

    def gen_contacts(self):
        current_length = self.current_length()
        if current_length == self.length:
            return []
        contact_pair = [self.particles[0], self.particles[1]]
        p_sep = self.particles[1].physics.p - self.particles[0].physics.p
        normal = p_sep/np.linalg.norm(p_sep)
        if current_length > self.length:
            penetration = current_length - self.length
        else:
            normal = -1*normal
            penetration = self.length - current_length
        restitution = 0
        contact = pcontacts.ParticleContact(contact_pair,
                                            restitution, normal, penetration)
        return [contact]
