from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

<<<<<<< HEAD
def move_from_center_to_right():
    x, y = 800 // 2, 90
    while x < 800 - 25:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        x += 10
        delay(0.01)

def move_up():
    x, y = 800 - 25, 90
    while y < 600 - 50:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        y += 10
        delay(0.01)


def move_left():
    x, y = 800 - 25, 600 - 50
    while x > 0 + 25:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        x -= 10
        delay(0.01)

def move_down():
    x, y = 0 + 25, 600 - 50
    while y > 0 + 90:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        y -= 10
        delay(0.01)

def move_from_left_to_center():
    x, y = 0 + 25, 90
    while x < 800 // 2:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        x += 10
        delay(0.01)

def make_rectangle():

    move_from_center_to_right()
    move_up()
    move_left()
    move_down()
    move_from_left_to_center()


def make_circle():
    cx, cy = 800 // 2, 600 // 2
    r = (600 - 180) // 2
    degree = -90

    while degree < 270:
        clear_canvas_now()
        grass.draw_now(400, 30)
        radian = math.radians(degree)
        character.draw_now(math.cos(radian)*r + cx, math.sin(radian)*r + cy)
        degree += 1
        delay(0.01)

while True:
    make_rectangle()
    make_circle()
=======
#여기를 채워 넣으시오
>>>>>>> parent of ed0b5b2... Drill_05


close_canvas()
