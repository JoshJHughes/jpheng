import pyglet
import jpheng.entities as entities
import jpheng.window as window
import jpheng.maps as maps
import jpheng.force_generators as force
import numpy as np

# This demo is intended to showcase a single particle moving around the
# 'EmptyMap' level.  Press escape to exit the program.


if __name__ == '__main__':
    # create level map
    level_map = maps.EmptyMap()

    # create window
    # window = window.Window(level_map, caption="jpheng Demo", resizable=True,
    #                        fullscreen=True)
    window = window.Window(level_map, caption="jpheng Demo", resizable=True)

    # create particle
    p = [0, 0, 20]
    v = [70, 50, 0]
    a = [0, 0, 0]
    inv_mass = 1/5
    r = 1
    particle = entities.Particle(p, v, a, inv_mass, r, color=(187, 86, 103))
    window.add_entity(particle)

    test_generator = force.GravityGenerator(np.array([0, 0, -20]))
    particle.physics.add_generator(test_generator)

    # enter main program loop
    pyglet.app.run()
