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
            window.add_entity(entities.Laser(p, dir))

    # enter main program loop
    pyglet.app.run()
