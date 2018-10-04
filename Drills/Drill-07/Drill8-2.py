from pico2d import *
import random

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas(1280, 1024)

grass = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')

def Track_curve(i,p1,p2,p3,p4):
    pass

def goal_current_to_point(point_count):
    pass

def run_character():
    pass

cx, cy = 800 // 2, 90
p = [(random.randint(0 + 100, KPU_WIDTH - 100), random.randint(0 + 100, KPU_HEIGHT - 100)) for i in range(10)]

while True:
    run_character()

close_canvas()
