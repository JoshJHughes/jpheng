import pyglet
import numpy as np


# Fraction of velocity retained each second, required to remove energy added
# through numerical instability of the integrator.
damping = 0.995
# g = np.array([0, -9.81, 0])
g = np.zeros(3)


class Particle:
    """Class defining a point mass.
    """
    def __init__(self, p, v, a, inv_mass, r, n_lat=32, n_long=32, color=None):
        # physics properties
        self.p = np.array(p, dtype=float)  # position
        self.v = np.array(v, dtype=float)  # velocity
        self.a = np.array(a, dtype=float)  # acceleration
        self.inv_mass = inv_mass  # inverse mass
        self.r = r  # radius

        # drawing properties
        self.n_verts = n_lat*n_long  # number of vertices
        vertices = np.zeros(3*self.n_verts)  # 3 components per vertex
        indices = [0]*3*2*(n_lat-2)*n_long
        if color != None:
            self.color = color*self.n_verts
        else:
            self.color = np.random.randint(0, 256, 3*self.n_verts)

        # generate vertices about p
        for j in range(n_lat):
            for i in range(n_long):
                theta = np.pi*(1-j/(n_lat-1))
                phi = 2*np.pi*(i/n_long + j/(2*n_long))
                vertex = [r*np.sin(theta)*np.cos(phi)+p[0],
                          r*np.sin(theta)*np.sin(phi)+p[1],
                          r*np.cos(theta)+p[2]]
                vertices[3*(j*n_long+i):3+3*(j*n_long+i)] = vertex

        # generate indices
        for j in range(n_lat-2):
            for i in range(n_long-1):
                indices[6*(j*n_long+i)+0] = n_long+j*n_long+i
                indices[6*(j*n_long+i)+1] = n_long+(j-1)*n_long+i+1
                indices[6*(j*n_long+i)+2] = n_long+j*n_long+i+1
                indices[6*(j*n_long+i)+3] = n_long+j*n_long+i
                indices[6*(j*n_long+i)+4] = n_long+j*n_long+i+1
                indices[6*(j*n_long+i)+5] = n_long+(j+1)*n_long+i
            # do final column manually
            i = n_long-1
            indices[6*(j*n_long+i)+0] = n_long+j*n_long+i
            indices[6*(j*n_long+i)+1] = n_long+(j-1)*n_long
            indices[6*(j*n_long+i)+2] = n_long+j*n_long
            indices[6*(j*n_long+i)+3] = n_long+j*n_long+i
            indices[6*(j*n_long+i)+4] = n_long+j*n_long
            indices[6*(j*n_long+i)+5] = n_long+(j+1)*n_long+i

        self.vertex_list_indexed = pyglet.graphics.vertex_list_indexed(
            self.n_verts, indices, ('v3f', vertices), ('c3B', self.color))

    def draw(self):
        self.vertex_list_indexed.draw(pyglet.gl.GL_TRIANGLES)

    def update(self, dt):
        """Calculate the new position, velocity and acceleration of the
        particle based on its acceleration.  Uses simple Euler integration
        method.
        """
        # update position based on last step's velocity and acceleration
        dp = self.v*dt + 0.5*self.a*dt**2
        self.p += dp
        # update velocity based on last step's acceleration, reduce previous
        # step's velocity by damping**dt to avoid numerical instability
        self.v = self.v*(damping**dt) + self.a*dt
        # set acceleration to current acceleration
        self.a = g
        # update vertex list with new position
        self.vertex_list_indexed.vertices = np.add(
            self.vertex_list_indexed.vertices, np.tile(dp, self.n_verts))



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
