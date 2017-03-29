import pyglet


class EmptyMap:
    def __init__(self, x_lim=100, y_lim=100, wall_height=50):
        self.floor_level = 0
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.wall_height = wall_height

        floor_colors = (142, 219, 132)*4
        wall_colors = (50, 62, 66)*4

        floor_vertices = [
            -x_lim, -y_lim, self.floor_level,
             x_lim, -y_lim, self.floor_level,
             x_lim,  y_lim, self.floor_level,
            -x_lim,  y_lim, self.floor_level]
        wall1_vertices = [
            -x_lim, -y_lim, self.floor_level,
             x_lim, -y_lim, self.floor_level,
             x_lim, -y_lim, wall_height,
            -x_lim, -y_lim, wall_height]
        wall2_vertices = [
            x_lim, -y_lim, self.floor_level,
            x_lim,  y_lim, self.floor_level,
            x_lim,  y_lim, wall_height,
            x_lim, -y_lim, wall_height]
        wall3_vertices = [
             x_lim, y_lim, self.floor_level,
            -x_lim, y_lim, self.floor_level,
            -x_lim, y_lim, wall_height,
             x_lim, y_lim, wall_height]
        wall4_vertices = [
            -x_lim,  y_lim, self.floor_level,
            -x_lim, -y_lim, self.floor_level,
            -x_lim, -y_lim, wall_height,
            -x_lim,  y_lim, wall_height]

        self.boundary = pyglet.graphics.Batch()

        self.boundary.add(4, pyglet.gl.GL_QUADS,
            None, ('v3f', floor_vertices), ('c3B', floor_colors))
        self.boundary.add(4, pyglet.gl.GL_QUADS,
            None, ('v3f', wall1_vertices), ('c3B', wall_colors))
        self.boundary.add(4, pyglet.gl.GL_QUADS,
            None, ('v3f', wall2_vertices), ('c3B', wall_colors))
        self.boundary.add(4, pyglet.gl.GL_QUADS,
            None, ('v3f', wall3_vertices), ('c3B', wall_colors))
        self.boundary.add(4, pyglet.gl.GL_QUADS,
            None, ('v3f', wall4_vertices), ('c3B', wall_colors))

    def draw(self):
        self.boundary.draw()