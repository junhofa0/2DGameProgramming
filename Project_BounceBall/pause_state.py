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
    pass

def handle_events():
    pass

def draw():
    pass

def update():
    pass

def pause():
    pass

def resume():
    pass