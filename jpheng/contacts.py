import numpy as np

class EntityContact:
    """An EntityContact represents two entities in contact.  Resolving a
    contact removes interpenetration and applies sufficient impulse to keep
    them apart.  Colliding bodies may also rebound.

    This class's methods should not be called, to resolve a set of contacts
    use the EntityContactResolver class.
    Variables:
        entities: List containing the entities involved in the contact.
            If the second element is None then the collision is with a
            non-particle object, e.g. the scenery.
        restitution: Coefficient of restitution for the contact.  v_after =
            -restitution*v_before
        normal: The contact normal, 3D numpy array [x,y,z].  Given from the
            perspective of self.entities[0] (subscript a),  n = p_a - p_b
            for particles.  Must be normalised.
        penetration: The depth of penetration at the contact in the
            direction of the contact normal.  Positive for greater penetration.
        entity_movement: The amount that each of the two entities was moved
            during the interpenetration resolution.  Used by
            EntityContactResolver to update interpenetration depth without
            performing the collision detection a second time.
    Methods:
        resolve: Resolves contact for velocity and interpenetration
        calc_separation_velocity: Returns the separation velocity of the
            entities in contact
        resolve_velocity: Resolves the final velocity of each entity.
            Energy loss is described by the coefficient of restitution.
            Substitute the separation velocity into the equation for
            conservation of momentum to obtain:
            v_a' = v_a - (m_b/(m_a + m_b))*(1+c)*v_s*n
            v_b' = v_b + (m_a/(m_a + m_b))*(1+c)*v_s*n
            where c is the coefficient of restitution, v_s is the separation
            velocity, and n is the contact normal.
        resolve_interpenetration: Moves each entity apart along the contact
            normal so that they no longer penetrate each other.  Movement is
            done in proportion to the inverse masses of the entities.
            p_a' = p_a + (m_b/(m_a+m_b))*d*n
            p_b' = p_b - (m_a/(m_a+m_b))*d*n
            where d is the penetration depth and n is the contact normal
    """
    def __init__(self, entities, restitution, normal, penetration):
        self.entities = entities
        self.restitution = restitution
        self.normal = np.array(normal)
        self.penetration = penetration
        self.entity_movement = [np.zeros(3), np.zeros(3)]

    def resolve(self, duration):
        """Resolves this contact, for both velocity and interpenetration."""
        self.resolve_velocity(duration)
        self.resolve_interpenetration(duration)

    def calc_separation_velocity(self):
        """Calculates the separation velocity at this contact."""
        v_rel = self.entities[0].physics.v
        if self.entities[1] is not None:
            v_rel = v_rel - self.entities[1].physics.v
        return np.dot(v_rel,self.normal)

    def resolve_velocity(self, duration):
        """Handles the impulse calculations for this collision."""
        v_sep = self.calc_separation_velocity()
        # if v_sep >=0 then contact is either separating or stationary and
        #  no impulse is required
        if v_sep >= 0:
            return

        # calculate separation velocity after the collision
        new_v_sep = -self.restitution*v_sep

        # Check for the additional component of the new separation velocity
        # caused by acceleration in the direction of the contact normal in
        # the most recent step. This can cause jittering in resting contacts
        #  and is removed from the new separation velocity.
        # Get v caused by acceleration in direction of normal.
        v_acc = self.entities[0].physics.a
        if self.entities[1] is not None:
            v_acc = v_acc - self.entities[1].physics.a
        v_acc = np.dot(v_acc*duration, self.normal)

        # if we have a closing velocity caused by acceleration then remove
        # it, making sure we haven't removed more than there was to remove
        if v_acc < 0:
            new_v_sep += self.restitution*v_acc
            if new_v_sep < 0:
                new_v_sep = 0

        # calculate the change in separation velocity
        dv_sep = new_v_sep - v_sep

        # get total inverse mass
        total_inv_mass = self.entities[0].physics.inv_mass
        if self.entities[1] is not None:
            total_inv_mass += self.entities[1].physics.inv_mass
        # if all entities have infinite mass then there is no effect
        if total_inv_mass == 0: return

        # calculate changes in speed for each entity and apply them in the
        # direction of the contact normal
        dv_a = self.entities[0].physics.inv_mass*dv_sep/total_inv_mass
        self.entities[0].physics.v += dv_a*self.normal
        if self.entities[1] is not None:
            dv_b = self.entities[1].physics.inv_mass*dv_sep/total_inv_mass
            self.entities[1].physics.v -= dv_b*self.normal

    def resolve_interpenetration(self, duration):
        # if there is no penetration then return
        if self.penetration <= 0: return

        # get total inverse mass
        total_inv_mass = self.entities[0].physics.inv_mass
        if self.entities[1] is not None:
            total_inv_mass += self.entities[1].physics.inv_mass
        # if all entities have infinite mass then there is no effect
        if total_inv_mass == 0: return

        self.entity_movement[0] = self.entities[0].physics.inv_mass*\
                                  self.penetration*self.normal/total_inv_mass
        self.entities[0].physics.p += self.entity_movement[0]

        if self.entities[1] is not None:
            self.entity_movement[1] = self.entities[1].physics.inv_mass*\
                                    self.penetration*self.normal/total_inv_mass
            self.entities[1].physics.p -= self.entity_movement[1]

class EntityContactResolver:
    """Contact resolution algorithm for entity contacts.  One
    EntityContactResolver works for the entire simulation.
    Variables:
        max_iter: Maximum number of iterations used by the resolution
            algorithm.
    Methods:
        resolve_contacts: Resolves a given list of contacts.  If there are
            multiple contacts then resolves them in the order of ascending
            v_sep then in order of descending interpenetration if there are no
            contacts with v_sep < 0.  Adjusts penetration for every contact
            after each contact resolution.  If there are no contacts with
            v_sep < 0 or penetration > 0 then the algorithm returns.  While
            the algorithm can resolve penetrations caused by other collision
            resolutions it cannot register collisions with entities which do
            not already have a registered contact.
    """
    def __init__(self, max_iter):
        self.max_iter = max_iter

    def resolve_contacts(self, duration, contacts):
        n_contacts = len(contacts)
        iter = 0

        while iter < self.max_iter:
            min_v_sep = float('inf')
            min_v_sep_index = n_contacts
            max_penetration = -float('inf')
            max_penetration_index = n_contacts

            # find minimum separation velocity and maximum penetration depth
            for i in range(n_contacts):
                v_sep = contacts[i].calc_separation_vel()
                if v_sep < min_v_sep:
                    min_v_sep = v_sep
                    min_v_sep_index = i
                if contacts[i].penetration > max_penetration:
                    max_penetration = contacts[i].penetration
                    max_penetration_index = i

            # resolve contact with minimum v_sep first, then once there are
            # no contacts with negative v_sep resolve contact with maximum
            # penetration.  Repeat until either there are no contacts with
            # v_sep < 0 or max_pen > 0, or iter > max_iter.
            if min_v_sep < 0:
                contacts[min_v_sep_index].resolve(duration)
                index = min_v_sep_index

            elif max_penetration > 0:
                contacts[max_penetration_index].resolve(duration)
                index = max_penetration_index
            else:
                return

            # Once a contact has been resolved the entities in question may
            # have moved apart.  This could push them further into other
            # entities.  Adjust penetration depths for all other entities
            # in the list which were also contacting the moved entities.
            move = contacts[index].entity_movement
            for contact in contacts:
                if contact.entities[0] == contacts[index].entities[0]:
                    contact.penetration -= np.dot(move[0], contact.normal)
                elif contact.entities[0] == contacts[index].entities[1]:
                    contact.penetration -= np.dot(move[1], contact.normal)
                if contact.entities[1] is not None:
                    if contact.entities[1] == contacts[index].entities[0]:
                        contact.penetration += np.dot(move[0], contact.normal)
                    elif contact.entities[1] == contacts[index].entities[1]:
                        contact.penetration += np.dot(move[1], contact.normal)

            iter += 1