from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')


def reach_point(x, y, px, py):
    if (x > px - 5) and (x < px + 5) and (y > py - 5) and (y < py + 5):
        return True


def goal_current_to_point(point_count):
    point = [[203, 535], [132, 243], [535, 470], [477, 203], [715, 136], [316, 225], [510, 92], [692, 518], [682, 236],
             [712, 349]]
    frame = 0
    global x
    global y

    while True:
        clear_canvas_now()
        grass.draw(400,90)

        if point[point_count][0] - x > 0:
            direction = 1
        else:
            direction = -1

        if point_count == 0:
            x += (point[point_count][0] - x) / 6
            y += (point[point_count][1] - y) / 6
        else:
            x += (point[point_count][0] - point[point_count - 1][0]) / 10
            y += (point[point_count][1] - point[point_count -1][1]) / 10

        if direction > 0:
            character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
        elif direction < 0:
            character.clip_draw(frame * 100, 100 * 0, 100, 100, x, y)

        update_canvas()

        frame = (frame + 1) % 8

        delay(0.05)

        if reach_point(x, y, point[point_count][0], point[point_count][1]) == True :
            break


def run_character():
    point_count = 0

    while point_count < 10:

        goal_current_to_point(point_count)
        point_count += 1


x, y = 800 // 2, 90


while True:
    run_character()

close_canvas()

