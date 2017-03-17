import pyglet
import numpy as np
import jpheng.camera as cam
import jpheng.shapes as shapes


class JphengWindow(pyglet.window.Window):
    """Custom subclass of pyglet.window, adds a first person camera to the
    window as well as a list of all objects being drawn.
    """
    def __init__(self, *args, **kwargs):
        # call init of superclass (pyglet window)
        super(JphengWindow, self).__init__(*args, **kwargs)
        # set window properties (overwrites args)
        pyglet.gl.glClearColor(255, 255, 255, 1)
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        self.set_minimum_size(200, 200)
        # set camera
        self.camera = cam.FirstPersonCamera(self)
        # schedule camera updates
        pyglet.clock.schedule_interval(self.camera.update, 1/120)
        # create list of objects in window and schedule their updates
        self.shape_list = []
        pyglet.clock.schedule_interval(self.update, 1/60)

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
        for shape in self.shape_list:
            shape.draw()
        return pyglet.event.EVENT_HANDLED

    def update(self, dt):
        for shape in self.shape_list:
            shape.step(dt)

    def add_shape(self, shape):
        self.shape_list.append(shape)


if __name__ == '__main__':
    window = JphengWindow(caption="jpheng Demo", resizable=True)

    # create particle
    p = [0, 0, -8]
    v = [0, 0, 0]
    a = [0, 0, 0]
    inv_mass = 1/5
    r = 4
    particle = shapes.Particle(p, v, a, inv_mass, r)
    window.add_shape(particle)

    pyglet.app.run()
