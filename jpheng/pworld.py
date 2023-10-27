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
        self.contact_generators.append(pcontacts.BoundaryCollisionGenerator(
            self.particle_list, self.xlim, self.ylim, self.zlim))

    def step(self, dt):
        # update all forces
        self.force_registry.update_forces(dt)
        # step all particles
        for particle in self.particle_list:
            particle.step(dt)
        # generate contacts
        self.generate_contacts()
        # self.boundary_check(self.particle_list)
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
