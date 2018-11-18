import game_framework
import mapstage_state
import maptool
from pico2d import *

hide_cursor()
name = "LobbyState"
background_image = None
start_image = None
maptool_image = None
exit_image = None
mouse_image = None
mouse_click_image = None
mouse_x, mouse_y = None, None
start_x, start_y = 180, 380
maptool_x, maptool_y = 180, 245
exit_x, exit_y = 180, 110
start_on = False
maptool_on = False
exit_on = False
window_width, window_height = 1000, 600
button_width, button_height = 375, 110
mouse_down = False
lobby_bgm = False
click_bgm = None

def image_draw():
    background_image.draw(500, 300, 1000, 600)
    if start_on: start_image.draw(start_x + 30, start_y, button_width + 60, button_height + 20)
    else: start_image.draw(start_x, start_y, button_width , button_height)

    if maptool_on: maptool_image.draw(maptool_x + 30, maptool_y, button_width + 60, button_height + 20)
    else: maptool_image.draw(maptool_x, maptool_y, button_width, button_height)

    if exit_on: exit_image.draw(exit_x + 30, exit_y, button_width + 60, button_height + 20)
    else: exit_image.draw(exit_x, exit_y, button_width, button_height)

    if mouse_down: mouse_click_image.draw(mouse_x, mouse_y)
    else: mouse_image.draw(mouse_x, mouse_y)

def enter():
    global background_image
    global start_image
    global maptool_image
    global exit_image
    global mouse_image
    global mouse_click_image
    global lobby_bgm
    global click_bgm

    background_image = load_image("resource\\image\\lobby.png")
    start_image = load_image("resource\\image\\start_image.png")
    maptool_image = load_image("resource\\image\\map_editer_image.png")
    exit_image = load_image("resource\\image\\exit_image.png")
    mouse_image = load_image("resource\\image\\mouse.png")
    mouse_click_image = load_image("resource\\image\\mouse_click.png")

    lobby_bgm = load_music('resource\\sound\\lobby_bgm.ogg')
    lobby_bgm.set_volume(50)
    lobby_bgm.repeat_play()

    click_bgm = load_wav('resource\\sound\\selectmenu.ogg')
    click_bgm.set_volume(100)


def exit():
    global background_image
    global start_image
    global maptool_image
    global exit_image
    global mouse_image
    global mouse_click_image
    global lobby_bgm

    lobby_bgm.stop()

    del background_image
    del start_image
    del maptool_image
    del exit_image
    del mouse_image
    del mouse_click_image
    del lobby_bgm

def button_col():
    global mouse_x, mouse_y
    global start_x, start_y
    global maptool_x, maptool_y
    global exit_x, exit_y
    global start_on
    global maptool_on
    global exit_on
    global button_width, button_height

    if start_x - button_width // 2 < mouse_x < start_x + button_width // 2 and \
            start_y - button_height // 2 - 20 < mouse_y < start_y + button_height // 2 - 20:
        start_on = True
    else:
        start_on = False

    if maptool_x - button_width // 2 < mouse_x < maptool_x + button_width // 2 and \
            maptool_y - button_height // 2 - 20 < mouse_y < maptool_y + button_height // 2 - 20:
        maptool_on = True
    else:
        maptool_on = False

    if exit_x - button_width // 2 < mouse_x < exit_x + button_width // 2 and \
            exit_y - button_height // 2 - 20 < mouse_y < exit_y + button_height // 2 - 20:
        exit_on = True
    else:
        exit_on = False



def handle_events():
    global mouse_x
    global mouse_y
    global mouse_down
    global start_on
    global maptool_on
    global exit_on
    global click_bgm

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            if event.type == SDL_MOUSEMOTION:
                mouse_x, mouse_y = event.x, window_height - 1 - event.y
                button_col()
            if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
                mouse_down = True
                if start_on:
                    start_on = False
                    mouse_down = False
                    mapstage_state.mouse_x, mapstage_state.mouse_y = mouse_x, mouse_y
                    click_bgm.play()
                    game_framework.change_state(mapstage_state)
                if maptool_on:
                    maptool_on = False
                    mouse_down = False
                    maptool.mouse_x, maptool.mouse_y = mouse_x, mouse_y
                    click_bgm.play()
                    game_framework.change_state(maptool)
                if exit_on:
                    exit_on = False
                    mouse_down = False
                    game_framework.quit()
            if (event.type, event.button) == (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT):
                mouse_down = False


def draw():
    clear_canvas()
    image_draw()
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass
