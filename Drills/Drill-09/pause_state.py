import game_framework
import main_state
import title_state
from pico2d import *


name = "PauseState"
image = None
count = 0

def enter():
    global image
    image = load_image('pause.png')


def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.pop_state()


def draw():
    global count
    clear_canvas()
    if count % 200 > 100:
        image.draw(400, 300)
    main_state.boy.draw()
    main_state.grass.draw()
    update_canvas()


def update():
    global count
    count = (count+1) % 1000



def pause():
    pass


def resume():
    pass






