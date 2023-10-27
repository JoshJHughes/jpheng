import pyglet
import jpheng.particles as entities
import jpheng.window as windows
import jpheng.maps as maps
import numpy as np
from jpheng import pworld


# This demo is intended to showcase the 'firework' class which
# exhibits special behaviour.  Fireworks have a fuse, when the fuse runs out
#  the firework will 'die'.  If the firework was a parent it will spawn
# additional fireworks based on the code in the 'fireworks_rules' function.
#  If the firework was a child it will simply disappear.  Fireworks can be
# spawned by left-clicking on the mouse.

if __name__ == '__main__':
    xlim = [-100, 100]
    ylim = [-100, 100]
    zlim = [0, 50]

    world = pworld.ParticleWorld(xlim, ylim, zlim)

    # create level map
    level_map = maps.EmptyMap(xlim, ylim, zlim)
    # create window
    window = windows.Window(world, level_map, caption="jpheng Demo",
                            resizable=True,
                            fullscreen=True)
    window.set_exclusive_mouse(True)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        """When left mouse is pressed spawn a new firework with random
        trajectory."""
        if button == pyglet.window.mouse.LEFT:
            theta = np.random.uniform(0, 10*np.pi/180)
            phi = np.random.uniform(0, 2*np.pi)
            s = 100
            p = np.array([0,0,0])
            v = np.array([s*np.sin(theta)*np.cos(phi),
                          s*np.sin(theta)*np.sin(phi),
                          s*np.cos(theta)])
            fuse = np.random.normal(5, 0.5)
            world.add_particle(entities.Firework(p, v, fuse, parent=True))

    def fireworks_rules(dt):
        """Defines the rules by which the fireworks propagate."""
        # create list of fireworks out of all entities in the current scene
        fireworks = filter(lambda x: isinstance(x, entities.Firework),
                           world.particle_list)
        for firework in fireworks:
            # if fuse has burned out, kill the firework
            if firework.fuse <= 0:
                world.remove_particle(firework)
                # if the firework is a parent, spawn children
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
                        world.add_particle(entities.Firework(
                            firework.physics.p,
                            v_list[i], fuse_list[i],
                            np.random.choice([True, False]),
                            firework.generation + 1))


    pyglet.clock.schedule_interval(fireworks_rules, 1/60)

    # enter main program loop
    pyglet.app.run()
