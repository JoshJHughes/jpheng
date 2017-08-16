import pyglet
import jpheng.window as windows
from jpheng import pworld
from jpheng import particles
from jpheng import maps
from jpheng import pcontacts

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
    p1 = [0, 30, 20]
    v1 = [-120, -10, 0]
    a1 = [0, 0, 0]
    inv_mass1 = 1/10
    r1 = 10
    particle1 = particles.QuickParticle(p1, v1, a1, inv_mass1, r1, color=(187, 86,
                                                                          103))

    p2 = [0, -30, 20]
    v2 = [140, 5, 0]
    a2 = [0, 0, 0]
    inv_mass2 = 1/10
    r2 = 10
    particle2 = particles.QuickParticle(p2, v2, a2, inv_mass2, r2, color=(36, 96,
                                                                          201))

    p3 = [20, -30, 20]
    v3 = [65, 65, 0]
    a3 = [0, 0, 0]
    inv_mass3 = 1/10
    r3 = 10
    particle3 = particles.QuickParticle(p3, v3, a3, inv_mass3, r3)

    p4 = [13, 8, 20]
    v4 = [79, -45, 0]
    a4 = [0, 0, 0]
    inv_mass4 = 1/10
    r4 = 10
    particle4 = particles.QuickParticle(p4, v4, a4, inv_mass4, r4)

    p5 = [2, -27, 20]
    v5 = [-32, 165, 0]
    a5 = [0, 0, 0]
    inv_mass5 = 1/10
    r5 = 10
    particle5 = particles.QuickParticle(p5, v5, a5, inv_mass5, r5)

    p6 = [35, -28, 20]
    v6 = [21, 14, 0]
    a6 = [0, 0, 0]
    inv_mass6 = 1/10
    r6 = 10
    particle6 = particles.QuickParticle(p6, v6, a6, inv_mass6, r6)

    p7 = [5, -8, 20]
    v7 = [2, 94, 0]
    a7 = [0, 0, 0]
    inv_mass7 = 1 / 10
    r7 = 10
    particle7 = particles.QuickParticle(p7, v7, a7, inv_mass7, r7)

    p8 = [18, 18, 20]
    v8 = [-30, 14, 0]
    a8 = [0, 0, 0]
    inv_mass8 = 1 / 10
    r8 = 10
    particle8 = particles.QuickParticle(p8, v8, a8, inv_mass8, r8)

    p9 = [-37, 38, 20]
    v9 = [-26, 78, 0]
    a9 = [0, 0, 0]
    inv_mass9 = 1 / 10
    r9 = 10
    particle9 = particles.QuickParticle(p9, v9, a9, inv_mass9, r9)

    p10 = [-6, -8, 20]
    v10 = [0, -144, 0]
    a10 = [0, 0, 0]
    inv_mass10 = 1 / 10
    r10 = 10
    particle10 = particles.QuickParticle(p10, v10, a10, inv_mass10, r10)

    p11 = [24, -28, 20]
    v11 = [-32, -64, 0]
    a11 = [0, 0, 0]
    inv_mass11 = 1 / 10
    r11 = 10
    particle11 = particles.QuickParticle(p11, v11, a11, inv_mass11, r11)

    p12 = [14, 26, 20]
    v12 = [-74, -34, 0]
    a12 = [0, 0, 0]
    inv_mass12 = 1 / 10
    r12 = 10
    particle12 = particles.QuickParticle(p12, v12, a12, inv_mass12, r12)

    # resting particle
    pr = [0, 0, 60]
    vr = [70, -102, 0]
    ar = [0, 0, 0]
    inv_massr = 1/5
    rr = 10
    particler = particles.QuickParticle(pr, vr, ar, inv_massr, rr, color=(76, 96,
                                                                          201))

    # add particles to world
    world.add_particle(particle1)
    world.add_particle(particle2)
    world.add_particle(particle3)
    world.add_particle(particle4)
    world.add_particle(particle5)
    world.add_particle(particle6)
    world.add_particle(particle7)
    world.add_particle(particle8)
    world.add_particle(particle9)
    world.add_particle(particle10)
    world.add_particle(particle11)
    world.add_particle(particle12)
    world.add_particle(particler)

    # hacked together to test resting contacts
    def resting_contact_test(duration, particle):
        if (particle.physics.p[2] - particle.graphics.r) <= 50:
            entities = [particle, None]
            restitution = 1
            normal = [0,0,1]
            penetration = 50 - (particle.physics.p[2] - particle.graphics.r)
            contact = pcontacts.ParticleContact(entities, restitution, normal,
                                                penetration)
            contact.resolve(duration)
    pyglet.clock.schedule_interval(resting_contact_test, 1/120, particler)

    # create window
    # window = windows.Window(world, level_map, caption="jpheng Demo",
    #                         resizable=True,
    #                         fullscreen=True)
    # window.set_exclusive_mouse(True)
    window = windows.Window(world, level_map, caption="jpheng Demo",
                            resizable=True)
    # enter main program loop
    pyglet.app.run()
