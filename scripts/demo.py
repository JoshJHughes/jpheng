import pyglet
import jpheng.entities as entities
import jpheng.window as window
import jpheng.maps as maps
import numpy as np


if __name__ == '__main__':
    # create level map
    level_map = maps.EmptyMap()

    # create window
    window = window.Window(level_map, caption="jpheng Demo", resizable=True,
                           fullscreen=True)

    # create particle
    p = [0, 0, 20]
    v = [0, 0, 0]
    a = [0, 0, 0]
    inv_mass = 1/5
    r = 1
    particle = entities.Particle(p, v, a, inv_mass, r, color=(25, 86, 103))
    window.add_entity(particle)

    # enter main program loop
    pyglet.app.run()
