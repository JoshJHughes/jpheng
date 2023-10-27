import pyglet
import jpheng.particles as entities
import jpheng.window as windows
import jpheng.maps as maps
import jpheng.pfgen as force
import numpy as np
import jpheng.physics as phy
import jpheng.graphics as gra
from jpheng import pworld

# This demo is intended to showcase a single particle moving around the
# 'EmptyMap' level.  Press escape to exit the program.


if __name__ == '__main__':

    xlim = [-100, 100]
    ylim = [-100, 100]
    zlim = [0, 50]

    world = pworld.ParticleWorld(xlim, ylim, zlim)

    # create level map
    level_map = maps.EmptyMap(xlim, ylim, zlim)
    # create window
    window = windows.Window(world, level_map, caption="jpheng Demo",
                            resizable=True,
                            fullscreen=True)
    window.set_exclusive_mouse(True)

    # create particle
    p = [0, 0, 20]
    v = [70, 50, 0]
    a = [0, 0, 0]
    inv_mass = 1/5
    r = 1
    particle = entities.QuickParticle(p, v, a, inv_mass, r, color=(187, 86, 103))
    world.add_particle(particle)

    # enter main program loop
    pyglet.app.run()
