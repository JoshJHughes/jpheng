import numpy as np
import jpheng.pfgen as pfgen
import jpheng.pcontacts as pcontacts

class ParticleWorld:
    """Keeps track of a set of particles and provides the means to update
    them all."""
    def __init__(self, xlim, ylim, zlim):
        self.particle_list = []
        self.force_registry = pfgen.ParticleForceRegistry()
        self.contact_generators = []
        self.contacts = []
        self.xlim = xlim
        self.ylim = ylim
        self.zlim = zlim
        # create contact resolver
        # max_iter = 100
        # self.contact_resolver = contacts.ParticleContactResolver(max_iter)
        # enable collisions for all particles
        self.contact_generators.append(pcontacts.ParticleCollisionGenerator(
            self.particle_list))

    def step(self, dt):
        # update all forces
        self.force_registry.update_forces(dt)
        # step all particles
        for particle in self.particle_list:
            particle.step(dt)
        # generate contacts
        self.generate_contacts()
        self.boundary_check(self.particle_list)
        # process contacts
        for contact in self.contacts:
            contact.resolve(dt)
        self.contacts = []

    def add_particle(self, particle):
        """Add particle to scene."""
        self.particle_list.append(particle)

    def remove_particle(self, particle):
        """Remove particle from scene."""
        self.particle_list.remove(particle)

    def generate_contacts(self):
        """Generate all current contacts from the contact generators and
        append self.contacts with the results."""
        for generator in self.contact_generators:
            self.contacts = self.contacts + generator.gen_contacts()

    def boundary_check(self, particles):
        """Check if entity is within level bounds, if not, reflect it back."""
        for particle in particles:
            # x direction
            if particle.physics.p[0] <= self.xlim[0] + \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([1, 0, 0])
                penetration = self.xlim[0] + particle.graphics.r - \
                              particle.physics.p[0]
                self.contacts.append(pcontacts.ParticleContact(contact_pair,
                    restitution, normal, penetration))
            elif particle.physics.p[0] >= self.xlim[1] - \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([-1, 0, 0])
                penetration = self.xlim[1] - particle.graphics.r - \
                              particle.physics.p[0]
                self.contacts.append(pcontacts.ParticleContact(contact_pair,
                    restitution, normal, penetration))
            # y direction
            if particle.physics.p[1] <= self.ylim[0] + \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([0, 1, 0])
                penetration = self.ylim[0] + particle.graphics.r - \
                              particle.physics.p[1]
                self.contacts.append(pcontacts.ParticleContact(contact_pair,
                    restitution, normal, penetration))
            elif particle.physics.p[1] >= self.ylim[1] - \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([0, -1, 0])
                penetration = self.ylim[1] - particle.graphics.r - \
                              particle.physics.p[1]
                self.contacts.append(pcontacts.ParticleContact(contact_pair,
                    restitution, normal, penetration))
            # z direction
            if particle.physics.p[2] <= self.zlim[0] + \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([0, 0, 1])
                penetration = self.zlim[0] + \
                              particle.graphics.r - \
                              particle.physics.p[2]
                self.contacts.append(pcontacts.ParticleContact(contact_pair,
                    restitution, normal, penetration))
