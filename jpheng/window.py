import pyglet
import numpy as np
from jpheng import camera as cam
from jpheng import pfgen as force
from jpheng import pcontacts as contacts


class Window(pyglet.window.Window):
    """Custom subclass of pyglet.window.  This class handles the open window
    within the operating system (from pyglet.window) as well as the
    user-controlled camera, the current level map, the list of entities in
    the current level, the force registry, and the scheduling for the camera
    and physics update functions.
    Variables:
        camera: First person camera object
        level_map: Map object containing scenery for simulation
        registry: ParticleForceRegistry object containing all force registrations
        for entities
    Methods:
        set3D: Calls pyglet functions to allow 3D perspective
        on_draw: Runs when window is rendered
        update: Calls functions needed at each time step of simulation
        boundary_check: Checks if entity is within level bounds, if not,
            reflect it back
    """
    def __init__(self, world, level_map, *args, **kwargs):
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
        self.world = world
        # create list of objects in window and schedule their updates
        # schedule function calls
        pyglet.clock.schedule_interval(self.camera.update, 1/120)
        pyglet.clock.schedule_interval(self.world.step, 1/120)

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
        for particle in self.world.particle_list:
            particle.draw()
        self.set3D()
        return pyglet.event.EVENT_HANDLED