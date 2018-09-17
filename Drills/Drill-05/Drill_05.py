from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

def goal_current_to_point(point_count):
    point = ((203, 535), (132, 243), (535, 470), (477, 203), (715, 136), (316, 225), (510, 92), (692, 518), (682, 236),
             (712, 349))
    frame = 0
    x, y = 800 // 2, 90

def run_character():
    derection = 1
    point_count = 0

    while point_count < 10:

        goal_current_to_point(point_count)
        point_count += 1




while True:
    run_character()

close_canvas()

