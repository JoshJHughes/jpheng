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

    # Particle Spring
    # create particle1
    p1 = [40, -40, 10]
    v1 = [0, 0, 0]
    a1 = [0, 0, 0]
    inv_mass = 1/5
    r = 1
    particle1 = entities.Particle(p1, v1, a1, inv_mass, r, color=(97, 86, 103))
    # create particle2
    p2 = [-40, -40, 10]
    v2 = [0, 0, 0]
    a2 = [0, 0, 0]
    inv_mass = 1 / 5
    r = 1
    particle2 = entities.Particle(p2, v2, a2, inv_mass, r, color=(97, 86, 103))
    # create marker between particles
    pm1 = [0,-40,10]
    vm1 = [0,0,0]
    am1 = [0,0,0]
    marker1 = entities.Particle(pm1, vm1, am1, inv_mass, r, color=(0,0,0))

    # add spring force to particle1
    k1 = 3
    l01 = 70
    spring1 = force.ParticleSpring(particle2.physics, k1, l01)
    spring2 = force.ParticleSpring(particle1.physics, k1, l01)
    particle1.physics.add_generator(spring1)
    particle2.physics.add_generator(spring2)

    # Anchored Spring
    p3 = [40, 40, 10]
    v3 = [0,0,0]
    a3 = [0,0,0]
    particle3 = entities.Particle(p3, v3, a3, inv_mass, r, color=(97, 36, 83))
    pm2 = [0, 40, 10]
    vm2 = [0, 0, 0]
    am2 = [0, 0, 0]
    marker2 = entities.Particle(pm2, vm2, am2, inv_mass, r, color=(0,0,0))
    k2 = 3
    l02 = 30
    anchor = pm2
    anchored_spring = force.AnchoredSpring(anchor, k2, l02)
    particle3.physics.add_generator(anchored_spring)

    # Anchored Bungee
    p4 = [40, 0, 80]
    v4 = [0,0,0]
    a4 = [0,0,0]
    particle4 = entities.Particle(p4, v4, a4, inv_mass, r, color=(97,36,83))
    pm3 = [40, 0, 100]
    vm3 = [0,0,0]
    am3 = [0,0,0]
    marker3 = entities.Particle(pm3, vm3, am3, inv_mass, r, color=(0,0,0))
    k3 = 5
    l03 = 20
    anchor = pm3
    anchored_bungee = force.AnchoredBungee(anchor, k3, l03)
    particle4.physics.add_generator(anchored_bungee)

    # Anchored Stiff Spring
    p5 = [40, 50, 10]
    v5 = [0, 0, 0]
    a5 = [0, 0, 0]
    particle5 = entities.Particle(p5, v5, a5, inv_mass, r, color=(97, 36, 83))
    pm4 = [0, 50, 10]
    vm4 = [0, 0, 0]
    am4 = [0, 0, 0]
    marker4 = entities.Particle(pm4, vm4, am4, inv_mass, r, color=(0, 0, 0))
    k4 = 20
    damping = 0.1
    anchor = pm4
    anchored_spring = force.StiffAnchoredSpring(anchor, k4, damping)
    particle5.physics.add_generator(anchored_spring)

    # remove gravity from particles and markers
    particle1.physics.g = np.zeros(3)
    particle2.physics.g = np.zeros(3)
    particle3.physics.g = np.zeros(3)
    particle5.physics.g = np.zeros(3)
    marker1.physics.g = np.zeros(3)
    marker2.physics.g = np.zeros(3)
    marker3.physics.g = np.zeros(3)
    marker4.physics.g = np.zeros(3)
    # add particles to window
    window.add_entity(particle1)
    window.add_entity(particle2)
    window.add_entity(particle3)
    window.add_entity(particle4)
    window.add_entity(particle5)
    window.add_entity(marker1)
    window.add_entity(marker2)
    window.add_entity(marker3)
    window.add_entity(marker4)

    # enter main program loop
    pyglet.app.run()
