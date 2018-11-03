import game_framework
import lobby_state
from pico2d import *


name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    image = load_image('kpu_credit.png')


def exit():
    global image
    del(image)


def update():
    global logo_time

    if(logo_time > 1.0):
        loge_time = 0
        #game_framework.quit()
        lobby_state.mouse_x, lobby_state.mouse_y = 0, 0
        game_framework.change_state(lobby_state)
    delay(0.01)
    logo_time += 0.01


def draw():
    global image
    clear_canvas()
    image.draw(500, 300, 1000, 600)
    update_canvas()



def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass




