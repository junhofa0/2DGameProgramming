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
open_map_count = 4
total_map_count = 21
window_width, window_height = 800, 600
gap_x, gap_y = 132, 133     # 블록 버튼 같의 갭 차이
start_x, start_y = 98, 425      # 블록이 그려지는 첫 x, y 좌표
image_w, image_h = 105, 120     # 블록 이미지 크기
mapstage_bgm = None
click_bgm = None

def image_draw():
    global background_image
    global mouse_down
    global mouse_image, mouse_click_image
    global lock_map_image, unlock_map_image
    global map_list
    global gap_x, gap_y
    global start_x, start_y

    background_image.draw(500, 300, 1000, 600)
    for map in map_list:
        if map[2]:
            if map[3]:
                unlock_map_image.clip_draw(map[0]*100 + map[1]*700, 0, 100, 100, start_x + map[0]*gap_x,
                                           start_y - map[1]*gap_y, image_w + 25, image_h + 25)
            else:
                unlock_map_image.clip_draw(map[0] * 100 + map[1] * 700, 0, 100, 100, start_x + map[0] * gap_x,
                                           start_y - map[1] * gap_y, image_w, image_h)
        else:
            lock_map_image.draw(start_x + map[0]*gap_x, start_y - map[1]*gap_y, image_w, image_h)

    if mouse_down:
        mouse_click_image.draw(mouse_x, mouse_y)
    else:
        mouse_image.draw(mouse_x, mouse_y)


def button_col():
    global mouse_x, mouse_y
    global map_list

    for map in map_list:
        if start_x + map[0] * gap_x - image_w // 2 <= mouse_x <= gap_x + map[0] * gap_x + image_w // 2 and \
                start_y - map[1] * gap_y - image_h // 2 <= mouse_y <= start_y - map[1] * gap_y + image_h//2 and \
                map[2] == True:
            map[3] = True
        else:
            map[3] = False


def enter():
    global background_image
    global mouse_image
    global mouse_click_image
    global lock_map_image
    global unlock_map_image
    global map_list
    global open_map_count
    global total_map_count
    global mapstage_bgm
    global click_bgm

    x, y = 0, 0
    for i in range(total_map_count):
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

    mapstage_bgm = load_music('resource\\sound\\mapselect_bgm.ogg')
    mapstage_bgm.set_volume(40)
    mapstage_bgm.repeat_play()
    click_bgm = load_wav('resource\\sound\\selectmenu.ogg')
    click_bgm.set_volume(100)

def exit():
    global background_image
    global mouse_image
    global mouse_click_image
    global lock_map_image
    global unlock_map_image
    global map_list
    global mapstage_bgm
    global click_bgm

    mapstage_bgm.stop()

    del background_image
    del mouse_image
    del mouse_click_image
    del lock_map_image
    del unlock_map_image
    del mapstage_bgm
    del click_bgm
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
                        click_bgm.play()
                        main_state.current_play_stage = str(map[0] + map[1]*7 + 1)
                        mouse_down = False
                        game_framework.change_state(main_state)
            elif (event.type, event.button) == (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT):
                mouse_down = False



def pause(): pass


def resume(): pass
