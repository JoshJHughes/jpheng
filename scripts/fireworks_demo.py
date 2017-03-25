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
    # window.set_exclusive_mouse(True)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            theta = np.random.uniform(0, 10*np.pi/180)
            phi = np.random.uniform(0, 2*np.pi)
            s = 100
            p = np.array([0,0,0])
            v = np.array([s*np.sin(theta)*np.cos(phi),
                          s*np.sin(theta)*np.sin(phi),
                          s*np.cos(theta)])
            fuse = np.random.normal(5, 0.5)
            window.add_entity(entities.Firework(p, v, fuse, parent=True))

    def fireworks_rules(dt):
        fireworks = filter(lambda x: x.type == "firework", window.entity_list)
        for firework in fireworks:
            if firework.fuse <= 0:
                firework.alive = False
                if firework.parent:
                    n = 10
                    v = np.random.normal(10, 0.1)
                    v_list = np.zeros((n, 3))
                    thetas = np.random.uniform(0, np.pi, n)
                    phis = np.random.uniform(0, 2*np.pi, n)
                    v_list[:,0] = v*np.sin(thetas)*np.cos(phis)
                    v_list[:,1] = v*np.sin(thetas)*np.sin(phis)
                    v_list[:,2] = v*np.cos(thetas)
                    fuse_list = np.random.normal(1.5, 0.7, n)
                    for i in range(n):
                        window.add_entity(entities.Firework(firework.p,
                            v_list[i], fuse_list[i],
                            np.random.choice([True, False]),
                            firework.generation + 1))


    pyglet.clock.schedule_interval(fireworks_rules, 1/60)

    # enter main program loop
    pyglet.app.run()
