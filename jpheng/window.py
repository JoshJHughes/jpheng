import pyglet
import numpy as np
from jpheng import camera as cam


class Window(pyglet.window.Window):
    """Custom subclass of pyglet.window, adds a first person camera to the
    window as well as a list of all objects being drawn.
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
        # schedule camera updates
        pyglet.clock.schedule_interval(self.camera.update, 1/120)
        # set level map
        self.level_map = level_map
        # create list of objects in window and schedule their updates
        self.entity_list = []
        pyglet.clock.schedule_interval(self.update, 1/120)

    def set3D(self):
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.gluPerspective(70, self.width/float(self.height), .1, 1000)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
        pyglet.gl.glLoadIdentity()

    def on_draw(self):
        self.clear()
        self.set3D()
        self.camera.draw()
        self.level_map.draw()
        for entity in self.entity_list:
            entity.draw()
        return pyglet.event.EVENT_HANDLED

    def update(self, dt):
        self.entity_list = list(filter(lambda x: x.alive, self.entity_list))
        for entity in self.entity_list:
            self.boundary_check(entity)
            entity.step(dt)

    def add_entity(self, entity):
        self.entity_list.append(entity)

    def remove_entity(self, entity):
        entity.alive = False

    def boundary_check(self, entity):
        # x direction
        if entity.p[0] <= -self.level_map.x_lim + entity.r:
            dp = entity.p[0] - (-self.level_map.x_lim + entity.r)
            entity.move(np.array([-dp,0,0]))
            entity.v[0] = -entity.v[0]
        elif entity.p[0] >= self.level_map.x_lim - entity.r:
            dp = entity.p[0] - (self.level_map.x_lim - entity.r)
            entity.move(np.array([-dp,0,0]))
            entity.v[0] = -entity.v[0]
        # y direction
        if entity.p[1] <= -self.level_map.y_lim + entity.r:
            dp = entity.p[1] - (-self.level_map.y_lim + entity.r)
            entity.move(np.array([0,-dp,0]))
            entity.v[1] = -entity.v[1]
        elif entity.p[1] >= self.level_map.y_lim - entity.r:
            dp = entity.p[1] - (self.level_map.y_lim - entity.r)
            entity.move(np.array([0,-dp,0]))
            entity.v[1] = -entity.v[1]
        # z direction
        if entity.p[2] <= self.level_map.floor_level + entity.r:
            dp = entity.p[2] - (self.level_map.floor_level + entity.r)
            entity.move(np.array([0,0,-dp]))
            entity.v[2] = -entity.v[2]