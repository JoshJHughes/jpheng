import pyglet
import numpy as np
from jpheng import camera as cam
from jpheng import force_generators as force
from jpheng import contacts as contacts


class Window(pyglet.window.Window):
    """Custom subclass of pyglet.window.  This class handles the open window
    within the operating system (from pyglet.window) as well as the
    user-controlled camera, the current level map, the list of entities in
    the current level, the force registry, and the scheduling for the camera
    and physics update functions.
    Variables:
        camera: First person camera object
        level_map: Map object containing scenery for simulation
        entity_list: List of all entities currently in simulation
        registry: ForceRegistry object containing all force registrations
        for entities
    Methods:
        set3D: Calls pyglet functions to allow 3D perspective
        on_draw: Runs when window is rendered
        update: Calls functions needed at each time step of simulation
        add_entity: Adds entity to scene
        remove_entity: Removes entity from scene
        boundary_check: Checks if entity is within level bounds, if not,
            reflect it back
    """
    def __init__(self, level_map, *args, **kwargs):
        # call init of superclass (pyglet window)
        super(Window, self).__init__(*args, **kwargs)
        # set window properties (overwrites args)
        pyglet.gl.glClearColor(255, 255, 255, 1)
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        self.set_minimum_size(200, 200)
        # set camera
        self.camera = cam.MouseFirstPersonCamera(self, position=(90,90,-50))
        self.set_mouse_visible(False)
        # set level map
        self.level_map = level_map
        # create list of objects in window and schedule their updates
        self.entity_list = []
        # create contact resolver
        # max_iter = 100
        # self.contact_resolver = contacts.EntityContactResolver(max_iter)
        # schedule function calls
        pyglet.clock.schedule_interval(self.camera.update, 1/120)
        pyglet.clock.schedule_interval(self.update, 1/120)

    def set3D(self):
        """Calls pyglet functions to allow 3D perspective."""
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.gluPerspective(70, self.width/float(self.height), .1, 1000)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
        pyglet.gl.glLoadIdentity()

    def on_draw(self):
        """Evaluate these functions when the window renders."""
        # clear scene
        self.clear()
        # self.set3D()
        # transform scene to new camera perspective
        self.camera.draw()
        # draw level map
        self.level_map.draw()
        # draw all entities
        for entity in self.entity_list:
            entity.draw()
        self.set3D()
        return pyglet.event.EVENT_HANDLED

    def update(self, dt):
        """Call functions needed at each time step of simulation."""
        # for each entity, check if in level bounds then call entity update
        # function
        contact_list = contacts.detect_particle_contacts(self.entity_list)
        contact_list = contact_list + self.boundary_check(self.entity_list)
        for contact in contact_list:
            contact.resolve(dt)
        # self.contact_resolver.resolve_contacts(dt, contact_list)
        for entity in self.entity_list:
            # self.boundary_check_old(entity)
            entity.update(dt)

    def add_entity(self, entity):
        """Add entity to scene."""
        self.entity_list.append(entity)

    def remove_entity(self, entity):
        """Remove entity from scene."""
        self.entity_list.remove(entity)

    def boundary_check(self, particles):
        """Check if entity is within level bounds, if not, reflect it back."""
        contact_list = []
        for particle in particles:
            # x direction
            if particle.physics.p[0] <= -self.level_map.x_lim + \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([1, 0, 0])
                penetration = -self.level_map.x_lim + particle.graphics.r - \
                              particle.physics.p[0]
                contact_list.append(contacts.EntityContact(contact_pair,
                    restitution, normal, penetration))
            elif particle.physics.p[0] >= self.level_map.x_lim - \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([-1, 0, 0])
                penetration = self.level_map.x_lim - particle.graphics.r - \
                              particle.physics.p[0]
                contact_list.append(contacts.EntityContact(contact_pair,
                    restitution, normal, penetration))
            # y direction
            if particle.physics.p[1] <= -self.level_map.y_lim + \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([0, 1, 0])
                penetration = -self.level_map.y_lim + particle.graphics.r - \
                              particle.physics.p[1]
                contact_list.append(contacts.EntityContact(contact_pair,
                    restitution, normal, penetration))
            elif particle.physics.p[1] >= self.level_map.y_lim - \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([0, -1, 0])
                penetration = self.level_map.y_lim - particle.graphics.r - \
                              particle.physics.p[1]
                contact_list.append(contacts.EntityContact(contact_pair,
                    restitution, normal, penetration))
            # z direction
            if particle.physics.p[2] <= self.level_map.floor_level + \
            particle.graphics.r:
                contact_pair = [particle, None]
                restitution = 1
                normal = np.array([0, 0, 1])
                penetration = self.level_map.floor_level + \
                              particle.graphics.r - \
                              particle.physics.p[2]
                contact_list.append(contacts.EntityContact(contact_pair,
                    restitution, normal, penetration))
        return contact_list

# this function should ultimately be handled by collision code
    def boundary_check_old(self, entity):
        """Check if entity is within level bounds, if not, reflect it back."""
        # x direction
        if entity.physics.p[0] <= -self.level_map.x_lim + entity.graphics.r:
            dp = entity.physics.p[0] - (-self.level_map.x_lim +
                                        entity.graphics.r)
            entity.physics.p += np.array([-dp,0,0])
            entity.physics.v[0] = -entity.physics.v[0]
        elif entity.physics.p[0] >= self.level_map.x_lim - entity.graphics.r:
            dp = entity.physics.p[0] - (self.level_map.x_lim -
                                        entity.graphics.r)
            entity.physics.p += np.array([-dp,0,0])
            entity.physics.v[0] = -entity.physics.v[0]
        # y direction
        if entity.physics.p[1] <= -self.level_map.y_lim + entity.graphics.r:
            dp = entity.physics.p[1] - (-self.level_map.y_lim +
                                        entity.graphics.r)
            entity.physics.p += np.array([0,-dp,0])
            entity.physics.v[1] = -entity.physics.v[1]
        elif entity.physics.p[1] >= self.level_map.y_lim - entity.graphics.r:
            dp = entity.physics.p[1] - (self.level_map.y_lim -
                                        entity.graphics.r)
            entity.physics.p += np.array([0,-dp,0])
            entity.physics.v[1] = -entity.physics.v[1]
        # z direction
        if entity.physics.p[2] <= self.level_map.floor_level + \
                entity.graphics.r:
            dp = entity.physics.p[2] - (self.level_map.floor_level +
                                        entity.graphics.r)
            entity.physics.p += np.array([0,0,-dp])
            entity.physics.v[2] = -entity.physics.v[2]