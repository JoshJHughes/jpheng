import pyglet
import jpheng.entities as entities
import jpheng.window as windows
import jpheng.maps as maps
import jpheng.force_generators as force
import numpy as np
import jpheng.physics as phy
import jpheng.graphics as gra

# This demo is intended to showcase a single particle moving around the
# 'EmptyMap' level.  Press escape to exit the program.


if __name__ == '__main__':
    # create level map
    level_map = maps.EmptyMap()

    # create window
    # window = window.Window(level_map, caption="jpheng Demo", resizable=True,
    #                        fullscreen=True)

    # EXCLUSIVE MOUSE
    window = windows.Window(level_map, mouse_sensitivity=0.005,
                            caption="jpheng Demo",
                            resizable=True)
    window.set_exclusive_mouse(True)

    # NON-EXCLUSIVE MOUSE
    # window = windows.Window(level_map, caption="jpheng Demo", resizable=True)

    # create particle
    p = [0, 0, 20]
    v = [70, 50, 0]
    a = [0, 0, 0]
    inv_mass = 1/5
    r = 1
    particle = entities.Particle(p, v, a, inv_mass, r, color=(187, 86, 103))
    window.add_entity(particle)

    # enter main program loop
    pyglet.app.run()
