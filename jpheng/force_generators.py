class ForceGenerator:
    """Interface for generator used to add forces to one or more particles.
    Methods:
        update_force: Update the force accumulator in the entity based on a
            time step of 'duration'.
    """
    def update_force(self, entity, duration):
        pass

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
        """Update force on entity after time step of 'duration'"""
        # objects with inv_mass = 0 are considered fixed in place
        if entity.inv_mass == 0:
            return
        else:
            entity.force_accum += self.g/entity.inv_mass