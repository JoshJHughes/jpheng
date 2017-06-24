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
    window = windows.Window(level_map, width = 800, height = 600,
                            caption="jpheng Demo", resizable=True)
    window.set_exclusive_mouse(True)

    # create particle1
    p1 = [40, -20, 10]
    v1 = [0, 10, 0]
    a1 = [0, 0, 0]
    inv_mass = 1/5
    r = 1
    particle1 = entities.Particle(p1, v1, a1, inv_mass, r, color=(187, 86,
                                                                  103))
    # create particle2
    p2 = [-40, 20, 40]
    v2 = [0, 10, 0]
    a2 = [0, 0, 0]
    inv_mass = 1 / 5
    r = 1
    particle2 = entities.Particle(p2, v2, a2, inv_mass, r, color=(187, 86,
                                                                  103))

    # create marker between particles
    pm = [0,0,20]
    vm = [0,0,0]
    am = [0,0,0]
    marker = entities.Particle(pm, vm, am, inv_mass, r, color=(0,0,0))

    # remove gravity from particles
    marker.physics.g = np.zeros(3)

    # add spring force to particle1
    k = 10
    l0 = 70
    spring1 = force.ParticleSpring(particle2.physics, k, l0)
    spring2 = force.ParticleSpring(particle1.physics, k, l0)
    particle1.physics.add_generator(spring1)
    particle2.physics.add_generator(spring2)


    # add particles to window
    window.add_entity(particle1)
    window.add_entity(particle2)
    window.add_entity(marker)

    # enter main program loop
    pyglet.app.run()
