import numpy as np
import pyglet

class GraphicsComponent:
    """Class which contains state and methods to describe, manipulate,
    and update a shape.  Initially vertex_list is centred on the origin,
    this is corrected the first time update is run.
    Variables:
        n_verts: Number of vertices in the sphere
        draw_mode: OpenGL draw mode for the vertex_list
        vertex_list: Indexed vertex list containing the vertices and
            colours of the sphere
        color: RGB tuple containing the shape's color
        mesh: Numpy array containing the positions of the shape's vertices
            relative to its centre
    Methods:
        draw: Draws the shape in the active pyglet window
        update: Moves the shape to be centered around the position of entity
    """
    def __init__(self):
        self.vertex_list = None
        self.color = None
        self.n_verts = None
        self.draw_mode = None
        self.mesh = None

    def draw(self):
        """Draw mesh."""
        self.vertex_list.draw(self.draw_mode)

    def update(self, entity, dt):
        """Update the vertex list to the new entity position."""
        self.vertex_list.vertices = np.add(
            self.mesh, np.tile(entity.physics.p, self.n_verts))

class SphereComponent(GraphicsComponent):
    """Graphics component to describe a sphere."""
    def __init__(self, r, color=None):
        GraphicsComponent.__init__(self)
        # number of latitudinal and longitudinal vertex positions
        n_lat = int(min(20, 3 + r))
        n_long = int(min(30, 5 + r))
        # set state
        self.r = r  # radius
        self.n_verts = n_lat*n_long  # number of vertices
        self.draw_mode = pyglet.gl.GL_TRIANGLES  # pyglet draw mode
        if color == None:
            color = np.random.randint(0, 256, 3)
        self.color = color  # color rgb tuple

        self.mesh = np.zeros(3*self.n_verts)  # 3 components per vertex
        indices = [0]*3*2*(n_lat - 2)*n_long
        colors = color*self.n_verts

        # generate vertices about origin
        for j in range(n_lat):
            for i in range(n_long):
                theta = np.pi*(1 - j/(n_lat - 1))
                phi = 2*np.pi*(i/n_long + j/(2*n_long))
                vertex = [r*np.sin(theta)*np.cos(phi),
                          r*np.sin(theta)*np.sin(phi),
                          r*np.cos(theta)]
                self.mesh[3*(j*n_long + i):3 + 3*(j*n_long + i)] = vertex
        vertices = self.mesh

        # generate indices
        for j in range(n_lat - 2):
            for i in range(n_long - 1):
                indices[6*(j*n_long + i) + 0] = n_long + j*n_long + i
                indices[6*(j*n_long + i) + 1] = n_long + (j - 1)*n_long + i + 1
                indices[6*(j*n_long + i) + 2] = n_long + j*n_long + i + 1
                indices[6*(j*n_long + i) + 3] = n_long + j*n_long + i
                indices[6*(j*n_long + i) + 4] = n_long + j*n_long + i + 1
                indices[6*(j*n_long + i) + 5] = n_long + (j + 1)*n_long + i
            # do final column manually
            i = n_long - 1
            indices[6*(j*n_long + i) + 0] = n_long + j*n_long + i
            indices[6*(j*n_long + i) + 1] = n_long + (j - 1)*n_long
            indices[6*(j*n_long + i) + 2] = n_long + j*n_long
            indices[6*(j*n_long + i) + 3] = n_long + j*n_long + i
            indices[6*(j*n_long + i) + 4] = n_long + j*n_long
            indices[6*(j*n_long + i) + 5] = n_long + (j + 1)*n_long + i

        self.vertex_list = pyglet.graphics.vertex_list_indexed(
            self.n_verts, indices, ('v3f', vertices), ('c3B', colors))

class CubeComponent(GraphicsComponent):
    """Graphics component to describe a cube."""
    def __init__(self, r, color=None):
        GraphicsComponent.__init__(self)
        self.n_verts = 8
        self.r = r  # side length
        self.draw_mode = pyglet.gl.GL_QUADS
        if color == None:
            color = np.random.randint(0, 256, 3)
        self.color = color

        self.mesh = np.array([
            -0.5, -0.5, -0.5,  # 0
            0.5, -0.5, -0.5,  # 1
            0.5, 0.5, -0.5,  # 2
            -0.5, 0.5, -0.5,  # 3
            -0.5, 0.5, 0.5,  # 4
            -0.5, -0.5, 0.5,  # 5
            0.5, -0.5, 0.5,  # 6
            0.5, 0.5, 0.5])  # 7
        self.mesh *= self.r

        vertices = self.mesh
        indices = [
            0, 1, 6, 5,  # front
            1, 2, 7, 6,  # right
            2, 3, 4, 7,  # back
            3, 0, 5, 4,  # left
            0, 1, 2, 3,  # bottom
            4, 5, 6, 7]  # top
        colors = color*self.n_verts

        self.vertex_list = pyglet.graphics.vertex_list_indexed(
            self.n_verts, indices, ('v3f', vertices), ('c3B', colors))