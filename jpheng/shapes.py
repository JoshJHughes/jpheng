import pyglet
import numpy as np


class Particle:
    """Class defining a point mass.
    """
    def __init__(self):
        self.p = np.zeros(3)  # position
        self.v = np.zeros(3)  # velocity
        self.a = np.zeros(3)  # acceleration
        # Fraction of velocity remaining after a single integration step,
        # required to remove energy added through numerical instability of
        # the integrator.
        self.damping = 0.995
        


class Cube:
    """Class defining a cube
    Variables:
        n_verts: Number of vertices in the cube
        side_length: Length of the cube side
        vertex_list_indexed: Indexed vertex list containing the vertices and
            colours of the cube
    Methods:
        draw: Draws the cube in the active pyglet window
        step: Moves the cube based on given velocity and dt
    """
    def __init__(self, side_length):
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
            0, 0, 0,   # 0
            1, 0, 0,   # 1
            1, 1, 0,   # 2
            0, 1, 0,   # 3
            0, 1, 1,   # 4
            0, 0, 1,   # 5
            1, 0, 1,   # 6
            1, 1, 1])  # 7
        vertices = vertices*side_length
        indices = [
            0, 1, 6, 5,  # front
            1, 2, 7, 6,  # right
            2, 3, 4, 7,  # back
            3, 0, 5, 4,  # left
            0, 1, 2, 3,  # bottom
            4, 5, 6, 7]  # top

        self.n_verts = 8
        self.side_length = side_length
        self.vertex_list_indexed = pyglet.graphics.vertex_list_indexed(
            self.n_verts, indices, ('v3f', vertices), ('c3B', colors))

    def draw(self):
        self.vertex_list_indexed.draw(pyglet.gl.GL_QUADS)

    def step(self, dt, v):
        step = np.tile(v, self.n_verts)*dt
        self.vertex_list_indexed.vertices = np.add(
            self.vertex_list_indexed.vertices, step)
