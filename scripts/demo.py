import pyglet
import numpy as np
import jpheng.camera as cam
import jpheng.shapes as shapes


class JphengWindow(pyglet.window.Window):
    """Custom subclass of pyglet.window, adds a first person camera to the
    window.
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
        # give cube
        self.cube = shapes.Cube(4)
        # schedule camera updates
        pyglet.clock.schedule_interval(self.camera.update, 1/120)
        self.v = np.array([3, 0, 0])
        pyglet.clock.schedule_interval(self.cube.step, 1/60, self.v)

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
        self.cube.draw()
        return pyglet.event.EVENT_HANDLED


if __name__ == '__main__':
    window = JphengWindow(caption="jpheng Demo", resizable=True)
    pyglet.app.run()
