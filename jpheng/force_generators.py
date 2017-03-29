class ForceGenerator:
    """Interface for generator used to add forces to one or more particles."""
    def update_force(self, entity, duration):
        pass


class ForceRegistry:
    """Holds all the force generators and the particles they apply to."""
    class Registration:
        """Keeps track of one force generator and the particle it applies
        to.
        """
        def __init__(self, entity, generator):
            self.entity = entity
            self.generator = generator

    def __init__(self):
        self.registry = []

    def add(self, entity, generator):
        self.registry.append(ForceRegistry.Registration(entity, generator))

    def remove(self, entity, generator):
        for entry in self.registry:
            if entry.entity == entity and entry.generator == \
                    generator:
                self.registry.remove(entry)

    def clear(self):
        self.registry = []

    def update_forces(self, duration):
        for entry in self.registry:
            entry.generator.update_force(entry.entity, duration)


class GravityGenerator(ForceGenerator):
    def __init__(self, gravity):
        self.g = gravity
    def update_force(self, entity, duration):
        if entity.inv_mass == 0:
            return
        else:
            entity.add_force(self.g/entity.inv_mass)