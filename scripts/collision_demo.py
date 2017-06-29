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

    # create particles
    p1 = [45, 2.5, 20]
    v1 = [-120, 0, 0]
    a1 = [0, 0, 0]
    inv_mass1 = 1/5
    r1 = 10
    particle1 = entities.Particle(p1, v1, a1, inv_mass1, r1, color=(187, 86,
                                                                  103))

    p2 = [-45, -3, 20]
    v2 = [140, 0, 0]
    a2 = [0, 0, 0]
    inv_mass2 = 1/10
    r2 = 10
    particle2 = entities.Particle(p2, v2, a2, inv_mass2, r2, color=(36, 96,
                                                                  201))
    # resting particle
    p3 = [0, 0, 60]
    v3 = [30, 0, 0]
    a3 = [0, 0, 0]
    inv_mass3 = 1/5
    r3 = 10
    particle3 = entities.Particle(p3, v3, a3, inv_mass3, r3, color=(36, 96,
                                                                    201))

    # add particles to window
    window.add_entity(particle1)
    window.add_entity(particle2)
    window.add_entity(particle3)

    # simple collision detection, to give a useful demo until proper routines
    #  are implemented
    def detect_collision(duration, entity1, entity2):
        p1 = entity1.physics.p
        p2 = entity2.physics.p

        r1 = entity1.graphics.r
        r2 = entity2.graphics.r

        p_sep = p1 - p2

        if np.abs(np.linalg.norm(p_sep)) < (r1 + r2):
            entities = [entity1, entity2]
            restitution = 1
            normal = p_sep/np.linalg.norm(p_sep)
            penetration = r1 + r2 - np.abs(np.linalg.norm(p_sep))
            contact = contacts.EntityContact(entities, restitution, normal,
                                             penetration)
            contact.resolve(duration)

    pyglet.clock.schedule_interval(detect_collision, 1/120,
                                   particle1, particle2)

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
    pyglet.clock.schedule_interval(resting_contact_test, 1/120, particle3)

    # enter main program loop
    pyglet.app.run()
