import pyglet
import jpheng.window as windows
from jpheng import pworld
from jpheng import particles
from jpheng import maps
from jpheng import pcontacts
from jpheng import plinks

# This demo is intended to showcase a single particle moving around the
# 'EmptyMap' level.  Press escape to exit the program.


if __name__ == '__main__':
    # create level map
    xlim = [-60, 60]
    ylim = [-60, 60]
    zlim = [0, 50]
    level_map = maps.EmptyMap(xlim, ylim, zlim)

    world = pworld.ParticleWorld(xlim, ylim, zlim)

    # create particles
    p1 = [0, 12.5, 20]
    v1 = [0, 0, 0]
    a1 = [0, 0, 0]
    inv_mass1 = 1/10
    r1 = 10
    particle1 = particles.QuickParticle(p1, v1, a1, inv_mass1, r1, color=(
        255, 0, 0))

    p2 = [0, -12.5, 20]
    v2 = [0, 0, 0]
    a2 = [0, 0, 0]
    inv_mass2 = 1/10
    r2 = 10
    particle2 = particles.QuickParticle(p2, v2, a2, inv_mass2, r2, color=(
        255, 0, 0))

    p3 = [0, 35, 20]
    v3 = [0, 20, 0]
    a3 = [0, 0, 0]
    inv_mass3 = 1/10
    r3 = 10
    particle3 = particles.QuickParticle(p3, v3, a3, inv_mass3, r3, color=(
        0, 0, 255))

    p5 = [-30, 12.5, 20]
    v5 = [0, 0, 0]
    a5 = [0, 0, 0]
    inv_mass5 = 1/20
    r5 = 10
    particle5 = particles.QuickParticle(p5, v5, a5, inv_mass5, r5, color=(
        255, 0, 0))

    p6 = [-30, 35, 20]
    v6 = [0, 20, 0]
    a6 = [0, 0, 0]
    inv_mass6 = 1/10
    r6 = 10
    particle6 = particles.QuickParticle(p6, v6, a6, inv_mass6, r6, color=(
        0, 0, 255))

    p7 = [30, 20, 30]
    v7 = [0, -10, 0]
    a7 = [0, 0, 0]
    inv_mass7 = 1/10
    r7 = 10
    particle7 = particles.QuickParticle(p7, v7, a7, inv_mass7, r7, color=(
        100, 120, 96))

    p8 = [30, -20, 30]
    v8 = [0, 0, 80]
    a8 = [0, 0, 0]
    inv_mass8 = 1 / 10
    r8 = 10
    particle8 = particles.QuickParticle(p8, v8, a8, inv_mass8, r8, color=(
        100, 120, 96))


    # add particles to world
    world.add_particle(particle1)
    world.add_particle(particle2)
    world.add_particle(particle3)
    world.add_particle(particle5)
    world.add_particle(particle6)
    world.add_particle(particle7)
    world.add_particle(particle8)

    # create rod between particles 1 and 2
    rod = plinks.ParticleRod([particle1, particle2], 25)
    world.contact_generators.append(rod)

    # create cable between particles 7 and 8
    cable = plinks.ParticleCable([particle8, particle7], 60, 0.7)
    world.contact_generators.append(cable)

    # create window
    window = windows.Window(world, level_map, caption="jpheng Demo",
                            resizable=True,
                            fullscreen=True)
    window.set_exclusive_mouse(True)
    # window = windows.Window(world, level_map, caption="jpheng Demo",
    #                         resizable=True)
    # enter main program loop
    pyglet.app.run()
