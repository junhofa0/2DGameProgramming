from pico2d import *
import random

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas(1280, 1024)

grass = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')


def Track_curve(i,p1,p2,p3,p4):
        t = i / 100
        x =  ((-t**3 + 2*t**2 - t)*p1[0] + (3*t**3 - 5*t**2 + 2)*p2[0] + (-3*t**3 + 4*t**2 + t)*p3[0] + (t**3 - t**2)*p4[0])/2
        y =  ((-t**3 + 2*t**2 - t)*p1[1] + (3*t**3 - 5*t**2 + 2)*p2[1] + (-3*t**3 + 4*t**2 + t)*p3[1] + (t**3 - t**2)*p4[1])/2
        return x, y

def goal_current_to_point(point_count):

    global p
    global cx
    global cy
    i = 0
    frame = 0

    while True:
        clear_canvas_now()
        grass.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)

        i += 2

        cx, cy = Track_curve(i, p[(point_count+9) % 10], p[point_count % 10],p[(point_count+1) % 10],p[(point_count+2) % 10])

        character.clip_draw(frame * 100, 100 * 0, 100, 100, cx, cy)

        update_canvas()
        frame = (frame + 1) % 8
        delay(0.02)

        if i == 100:
            break

def run_character():
    count = 0
    while True:
        goal_current_to_point(count)
        count = (count + 1) % 10


cx, cy = 800 // 2, 90
p = [(random.randint(0 + 100, KPU_WIDTH - 100), random.randint(0 + 100, KPU_HEIGHT - 100)) for i in range(10)]

while True:
    run_character()

close_canvas()

