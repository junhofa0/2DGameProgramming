import game_framework
import main_state
import game_world
import bounce_ball
from pico2d import *

name = "PauseState"

pause_image = None

# Ball Speed
PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm = 100pixel 1m
RUN_SPEED_MPS = 1.3
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # 1초에 1.3 METER = 130 PIXEL

def enter():
    global pause_image
    pause_image = load_image("resource\\image\\pause.png")

def exit():
    global pause_image
    main_state.start_time = get_time()
    del pause_image

def handle_events():
    pass

def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        if game_object == main_state.blocks:
            for block in game_object:
                block.draw()
        else:
            game_object.draw()

    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass