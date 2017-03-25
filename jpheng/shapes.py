import pyglet
import numpy as np


class Sphere:
    """Class defining a sphere."""
    def __init__(self, r, p, color=None):
        n_lat = int(min(20, 5 + r))
        n_long = int(min(30, 10 + r))
        self.r = r  # radius
        self.n_verts = n_lat*n_long  # number of vertices
        self.draw_mode = pyglet.gl.GL_TRIANGLES
        vertices = np.zeros(3*self.n_verts)  # 3 components per vertex
        indices = [0]*3*2*(n_lat-2)*n_long
        if color is not None:
            self.color = color*self.n_verts
        else:
            self.color = np.random.randint(0, 256, 3*self.n_verts)

        # generate vertices about origin
        for j in range(n_lat):
            for i in range(n_long):
                theta = np.pi*(1-j/(n_lat-1))
                phi = 2*np.pi*(i/n_long + j/(2*n_long))
                vertex = [r*np.sin(theta)*np.cos(phi) + p[0],
                          r*np.sin(theta)*np.sin(phi) + p[1],
                          r*np.cos(theta) + p[2]]
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

        self.vertex_list = pyglet.graphics.vertex_list_indexed(
            self.n_verts, indices, ('v3f', vertices), ('c3B', self.color))

    def draw(self):
        self.vertex_list.draw(self.draw_mode)

    def move(self, dp):
        """Move vertices by dp."""
        self.vertex_list.vertices = np.add(
            self.vertex_list.vertices, np.tile(dp, self.n_verts))



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
    def __init__(self, r, p, color=None):
        self.n_verts = 8
        self.side_length = r
        self.draw_mode = pyglet.gl.GL_QUADS
        if color is not None:
            colors = color*self.n_verts
        else:
            colors = np.random.randint(0, 256, 3*self.n_verts)

        vertices = np.array([
            -0.5, -0.5, -0.5,   # 0
             0.5, -0.5, -0.5,   # 1
             0.5,  0.5, -0.5,   # 2
            -0.5,  0.5, -0.5,   # 3
            -0.5,  0.5,  0.5,   # 4
            -0.5, -0.5,  0.5,   # 5
             0.5, -0.5,  0.5,   # 6
             0.5,  0.5,  0.5])  # 7
        vertices = vertices*r
        vertices[0::3] += p[0]
        vertices[1::3] += p[1]
        vertices[2::3] += p[2]
        indices = [
            0, 1, 6, 5,  # front
            1, 2, 7, 6,  # right
            2, 3, 4, 7,  # back
            3, 0, 5, 4,  # left
            0, 1, 2, 3,  # bottom
            4, 5, 6, 7]  # top

        self.vertex_list = pyglet.graphics.vertex_list_indexed(
            self.n_verts, indices, ('v3f', vertices), ('c3B', colors))

    def draw(self):
        self.vertex_list.draw(self.draw_mode)

    def move(self, dp):
        self.vertex_list.vertices = np.add(
            self.vertex_list.vertices, np.tile(dp, self.n_verts))
