import pyglet


class EmptyMap:
    """Simple empty map to run demos in.  Contains floor and four walls.
    Variables:
        xlim: Array containing [min, max] x-coordinate of the floor
        ylim: Array containing [min, max] y-coordinate of the floor
        zlim: Array containing [min, max] z co-ordinate of the walls
        boundary: pyglet batch containing the floor and wall vertices
    Methods:
        draw: Draw the map
    """
    def __init__(self, xlim=None, ylim=None, zlim=None):
        self.floor_level = 0
        if xlim is None:
            self.xlim = [-100, 100]
        self.x_lim = xlim
        if ylim is None:
            self.ylim = [-100, 100]
        self.y_lim = ylim
        if zlim is None:
            self.zlim = [0, 50]
        self.zlim = zlim

        floor_colors = (142, 219, 132)*4
        wall_colors = (50, 62, 66)*4

        floor_vertices = [
            xlim[1], ylim[1], zlim[0],
             xlim[0], ylim[1], zlim[0],
             xlim[0],  ylim[0], zlim[0],
            xlim[1],  ylim[0], zlim[0]]
        wall1_vertices = [
            xlim[1], ylim[1], zlim[0],
             xlim[0], ylim[1], zlim[0],
             xlim[0], ylim[1], zlim[1],
            xlim[1], ylim[1], zlim[1]]
        wall2_vertices = [
            xlim[0], ylim[1], zlim[0],
            xlim[0],  ylim[0], zlim[0],
            xlim[0],  ylim[0], zlim[1],
            xlim[0], ylim[1], zlim[1]]
        wall3_vertices = [
             xlim[0], ylim[0], zlim[0],
            xlim[1], ylim[0], zlim[0],
            xlim[1], ylim[0], zlim[1],
             xlim[0], ylim[0], zlim[1]]
        wall4_vertices = [
            xlim[1],  ylim[0], zlim[0],
            xlim[1], ylim[1], zlim[0],
            xlim[1], ylim[1], zlim[1],
            xlim[1],  ylim[0], zlim[1]]

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
        """Draw map."""
        self.boundary.draw()
