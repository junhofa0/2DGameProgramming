import game_framework
import lobby_state
import main_state
import game_world
from pico2d import *

name = "MapStageState"

background_image = None
mouse_image = None
mouse_click_image = None
unlock_map_image = None
lock_map_image = None
mouse_x, mouse_y = None, None
mouse_down = False
map_list = []
open_map_count = 10
window_width, window_height = 800, 600
gap_x, gap_y = 132, 133
start_x, start_y = 98, 425
image_w, image_h = 105, 120

def image_draw():
    global background_image
    global mouse_down
    global mouse_image, mouse_click_image
    global lock_map_image, unlock_map_image
    global map_list
    global gap_x, gap_y
    global start_x, start_y

    background_image.draw(500, 300, 1000, 600)
    for button in map_list:
        if button[2] == True:
            if button[3]:
                unlock_map_image.clip_draw(button[0]*100 + button[1]*700, 0, 100, 100, start_x + button[0]*gap_x,
                                           start_y - button[1]*gap_y, image_w + 25, image_h + 25)
            else:
                unlock_map_image.clip_draw(button[0] * 100 + button[1] * 700, 0, 100, 100, start_x + button[0] * gap_x,
                                           start_y - button[1] * gap_y, image_w, image_h)
        else:
            lock_map_image.draw(start_x + button[0]*gap_x, start_y - button[1]*gap_y, image_w, image_h)

    if mouse_down:
        mouse_click_image.draw(mouse_x, mouse_y)
    else:
        mouse_image.draw(mouse_x, mouse_y)


def button_col():
    global mouse_x, mouse_y
    global map_list

    for button in map_list:
        if start_x + button[0] * gap_x - image_w // 2 <= mouse_x <= gap_x + button[0] * gap_x + image_w // 2 and \
                start_y - button[1] * gap_y - image_h // 2 <= mouse_y <= start_y - button[1] * gap_y + image_h//2 and \
                    button[2] == True:
            button[3] = True
        else:
            button[3] = False


def enter():
    global background_image
    global mouse_image
    global mouse_click_image
    global lock_map_image
    global unlock_map_image
    global map_list
    global open_map_count

    x, y = 0, 0
    for i in range(21):
        if x < open_map_count:
            map_list.append([x % 7, y, True, False])
        else:
            map_list.append([x % 7, y, False, False])
        x += 1
        if x % 7 == 0:
            y += 1


    background_image = load_image('resource\\image\\map_select.png')
    mouse_image = load_image("resource\\image\\mouse.png")
    mouse_click_image = load_image("resource\\image\\mouse_click.png")
    lock_map_image = load_image("resource\\image\\lock_map.png")
    unlock_map_image = load_image("resource\\image\\unlock_map.png")

def exit():
    global background_image
    global mouse_image
    global mouse_click_image
    global lock_map_image
    global unlock_map_image
    global map_list

    main_state.Ball.direction = 0

    del background_image
    del mouse_image
    del mouse_click_image
    del lock_map_image
    del unlock_map_image
    map_list.clear()




def update():
    pass


def draw():
    clear_canvas()
    image_draw()
    update_canvas()

def handle_events():
    global mouse_x
    global mouse_y
    global mouse_down
    global map_list
    global dire

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                lobby_state.mouse_x, lobby_state.mouse_y = mouse_x, mouse_y
                game_framework.change_state(lobby_state)
            elif event.type == SDL_MOUSEMOTION:
                mouse_x, mouse_y = event.x, window_height - 1 - event.y
                button_col()
            elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
                mouse_down = True
                for map in map_list:
                    if map[3] == True:
                        main_state.map = str(map[0] + map[1]*7 + 1)
                        mouse_down = False
                        game_framework.change_state(main_state)
            elif (event.type, event.button) == (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT):
                mouse_down = False



def pause(): pass


def resume(): pass
