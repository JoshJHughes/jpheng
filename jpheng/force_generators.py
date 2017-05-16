class ForceGenerator:
    """Interface for generator used to add forces to one or more particles.
    Methods:
        update_force: Update the force accumulator in the entity based on a
            time step of 'duration'.
    """
    def update_force(self, entity, duration):
        pass


class ForceRegistry:
    """Holds all the force generators and the particles they apply to.
    Defines a Registration to keep track of which forces act on which
    entities.
    Variables:
        registry: Specifies that a given force generator acts on a given entity
    Methods:
        add: Add a registration to the registry
        remove: Remove a registration from the registry
        clear: Clear registry of all registrations
        update_forces: Update all forces stored in the registry
    """
    class Registration:
        """Keeps track of one force generator and the particle it applies
        to.
        Variables:
            entity: an Entity
            generator: a ForceGenerator which acts on entity
        """
        def __init__(self, entity, generator):
            self.entity = entity
            self.generator = generator

    def __init__(self):
        self.registry = []

    def add(self, entity, generator):
        """Add registration to registry."""
        self.registry.append(ForceRegistry.Registration(entity, generator))

    def remove(self, entity, generator):
        """Remove registration from registry."""
        for entry in self.registry:
            if entry.entity == entity and entry.generator == \
                    generator:
                self.registry.remove(entry)

    def clear(self):
        """Clear registry of all registrations."""
        self.registry = []

    def update_forces(self, duration):
        """Update all forces in the registry using the time step 'duration'."""
        for entry in self.registry:
            entry.generator.update_force(entry.entity, duration)


# Gravity is hardcoded into entity class, this is for testing purposes only
class GravityGenerator(ForceGenerator):
    """Generator for gravity.
    Variables:
        g: Acceleration due to gravity
    Methods:
        update_force: Update the force accumulator in the entity based on a
            time step of 'duration'.
    """
    def __init__(self, gravity):
        self.g = gravity
    def update_force(self, entity, duration):
        """Calculate force on entity after time step of 'duration'"""
        # objects with inv_mass = 0 are considered fixed in place
        if entity.inv_mass == 0:
            return
        else:
            entity.add_force(self.g/entity.inv_mass)