import pyglet
import  numpy as np
from jpheng.camera import FirstPersonCamera

class Cube:
    def __init__(self):
        colors = (
            56, 89, 105,
            25, 79, 255,
            69, 204, 18,
            75, 154, 182,
            56, 274, 153,
            98, 50, 103,
            56, 254, 103,
            250, 89, 189)
        vertices = np.array([
            0, 0, 0,  # 0
            1, 0, 0,  # 1
            1, 1, 0,  # 2
            0, 1, 0,  # 3
            0, 1, 1,  # 4
            0, 0, 1,  # 5
            1, 0, 1,  # 6
            1, 1, 1]) # 7
        indices = [
            0,1,6,5,  # front
            1,2,7,6,  # right
            2,3,4,7,  # back
            3,0,5,4,  # left
            0,1,2,3,  # bottom
            4,5,6,7]  # top

        self.vertex_list_indexed = pyglet.graphics.vertex_list_indexed(8,
            indices, ('v3f', vertices), ('c3B', colors))
        x = 2


    def draw(self):
        self.vertex_list_indexed.draw(pyglet.gl.GL_QUADS)


class JphengWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        # call init of superclass (pyglet window)
        super(JphengWindow, self).__init__(*args, **kwargs)
        # set window properties (overwrites args)
        pyglet.gl.glClearColor(255, 255, 255, 1)
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        self.set_minimum_size(200, 200)
        # # fps counter
        # fps_font = pyglet.font.load('Arial', 12)
        # self.fps_display = pyglet.clock.ClockDisplay(font=fps_font)
        # set camera
        self.camera = FirstPersonCamera(self)
        # give cube
        self.cube = Cube()
        # schedule update function to be called as often as possible
        pyglet.clock.schedule(self.update)


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


    def update(self, dt):
        self.camera.update(dt)
        # Your update code here


if __name__ == '__main__':
    window = JphengWindow(caption="jpheng Demo", resizable=True)
    pyglet.app.run()