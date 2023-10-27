import pyglet
import jpheng.particles as entities
import jpheng.window as windows
import jpheng.maps as maps
import numpy as np
from jpheng import pworld

# This demo is intended to showcase the ballistics entities.  Left clicking
# the mouse will spawn a laser bullet in front of the camera, travelling
# forwards.

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
        if button == pyglet.window.mouse.LEFT:
            p = np.array(window.camera._position)
            p[0] = -p[0]
            p[1] = -p[1]
            p[2] = -p[2]
            yaw = window.camera._yaw
            pitch = window.camera._pitch
            x = np.sin(np.radians(yaw))*np.cos(np.radians(pitch-90))
            y = np.cos(np.radians(yaw))*np.cos(np.radians(pitch-90))
            z = np.sin(np.radians(pitch-90))
            dir = np.array([-x, -y, z])
            dir /= np.linalg.norm([x,y,z])
            world.add_particle(entities.Laser(p, dir))

    # enter main program loop
    pyglet.app.run()
