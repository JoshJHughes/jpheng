import pyglet
import jpheng.entities as entities
import jpheng.window as windows
import jpheng.maps as maps
import jpheng.force_generators as force
import numpy as np
import jpheng.physics as phy
import jpheng.graphics as gra
import jpheng.contacts as contacts

# This demo is intended to showcase a single particle moving around the
# 'EmptyMap' level.  Press escape to exit the program.


if __name__ == '__main__':
    # create level map
    level_map = maps.EmptyMap(x_lim = 60, y_lim = 60)

    # create window
    window = windows.Window(level_map, caption="jpheng Demo", resizable=True,
                            fullscreen=True)
    window.set_exclusive_mouse(True)
    # window = windows.Window(level_map, caption="jpheng Demo", resizable=True)

    # create particles
    p1 = [0, 30, 20]
    v1 = [-120, -10, 0]
    a1 = [0, 0, 0]
    inv_mass1 = 1/10
    r1 = 10
    particle1 = entities.Particle(p1, v1, a1, inv_mass1, r1, color=(187, 86,
                                                                  103))

    p2 = [0, -30, 20]
    v2 = [140, 5, 0]
    a2 = [0, 0, 0]
    inv_mass2 = 1/10
    r2 = 10
    particle2 = entities.Particle(p2, v2, a2, inv_mass2, r2, color=(36, 96,
                                                                  201))

    p3 = [20, -30, 20]
    v3 = [65, 65, 0]
    a3 = [0, 0, 0]
    inv_mass3 = 1/10
    r3 = 10
    particle3 = entities.Particle(p3, v3, a3, inv_mass3, r3)

    p4 = [13, 8, 20]
    v4 = [79, -45, 0]
    a4 = [0, 0, 0]
    inv_mass4 = 1/10
    r4 = 10
    particle4 = entities.Particle(p4, v4, a4, inv_mass4, r4)

    p5 = [2, -27, 20]
    v5 = [-32, 165, 0]
    a5 = [0, 0, 0]
    inv_mass5 = 1/10
    r5 = 10
    particle5 = entities.Particle(p5, v5, a5, inv_mass5, r5)

    p6 = [35, -28, 20]
    v6 = [21, 14, 0]
    a6 = [0, 0, 0]
    inv_mass6 = 1/10
    r6 = 10
    particle6 = entities.Particle(p6, v6, a6, inv_mass6, r6)

    p7 = [5, -8, 20]
    v7 = [2, 94, 0]
    a7 = [0, 0, 0]
    inv_mass7 = 1 / 10
    r7 = 10
    particle7 = entities.Particle(p7, v7, a7, inv_mass7, r7)

    p8 = [18, 18, 20]
    v8 = [-30, 14, 0]
    a8 = [0, 0, 0]
    inv_mass8 = 1 / 10
    r8 = 10
    particle8 = entities.Particle(p8, v8, a8, inv_mass8, r8)

    p9 = [-37, 38, 20]
    v9 = [-26, 78, 0]
    a9 = [0, 0, 0]
    inv_mass9 = 1 / 10
    r9 = 10
    particle9 = entities.Particle(p9, v9, a9, inv_mass9, r9)

    p10 = [-6, -8, 20]
    v10 = [0, -144, 0]
    a10 = [0, 0, 0]
    inv_mass10 = 1 / 10
    r10 = 10
    particle10 = entities.Particle(p10, v10, a10, inv_mass10, r10)

    p11 = [24, -28, 20]
    v11 = [-32, -64, 0]
    a11 = [0, 0, 0]
    inv_mass11 = 1 / 10
    r11 = 10
    particle11 = entities.Particle(p11, v11, a11, inv_mass11, r11)

    p12 = [14, 26, 20]
    v12 = [-74, -34, 0]
    a12 = [0, 0, 0]
    inv_mass12 = 1 / 10
    r12 = 10
    particle12 = entities.Particle(p12, v12, a12, inv_mass12, r12)
    
    # resting particle
    pr = [0, 0, 60]
    vr = [70, -102, 0]
    ar = [0, 0, 0]
    inv_massr = 1/5
    rr = 10
    particler = entities.Particle(pr, vr, ar, inv_massr, rr, color=(76, 96,
                                                                    201))

    # add particles to window
    window.add_entity(particle1)
    window.add_entity(particle2)
    window.add_entity(particle3)
    window.add_entity(particle4)
    window.add_entity(particle5)
    window.add_entity(particle6)
    window.add_entity(particle7)
    window.add_entity(particle8)
    window.add_entity(particle9)
    window.add_entity(particle10)
    window.add_entity(particle11)
    window.add_entity(particle12)
    window.add_entity(particler)

    # hacked together to test resting contacts
    def resting_contact_test(duration, entity):
        if (entity.physics.p[2] - entity.graphics.r) <= 50:
            entities = [entity, None]
            restitution = 1
            normal = [0,0,1]
            penetration = 50 - (entity.physics.p[2] - entity.graphics.r)
            contact = contacts.EntityContact(entities, restitution, normal,
                                             penetration)
            contact.resolve(duration)
    pyglet.clock.schedule_interval(resting_contact_test, 1/120, particler)

    # enter main program loop
    pyglet.app.run()
