import game_framework
import pico2d

import start_state

pico2d.open_canvas(1000, 600)
pico2d.hide_cursor()
game_framework.run(start_state)
pico2d.close_canvas()

