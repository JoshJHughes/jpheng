import pyglet
import jpheng.entities as entities
import jpheng.window as window
import jpheng.maps as maps


if __name__ == '__main__':
    # create level map
    level_map = maps.EmptyMap()

    # create window
    window = window.Window(level_map, caption="jpheng Demo", resizable=True)

    # create particle
    p = [0, 0, 25]
    v = [100, 150, 0]
    a = [0, 0, 0]
    inv_mass = 1/5
    r = 5
    particle = entities.Particle(p, v, a, inv_mass, r)
    window.add_entity(particle)

    # enter main program loop
    pyglet.app.run()
