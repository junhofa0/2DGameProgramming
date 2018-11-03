import random
import json
import os

from pico2d import *
import game_framework
#import game_world

from bounce_ball import *
from block import *
from star import *

# Ball Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


name = "MainState"

ball = None
blocks = []
star = None
map = ''

def load_map():

    global ball
    global star
    global blocks
    global map

    fname = "map\\map" + map + ".txt"
    f = open(fname, 'r')

    line = f.readline()
    ball.x = int(line)
    line = f.readline()
    ball.y = int(line)

    ball.jump_now(8)
    ball.handle = True
    ball.boost = False
    ball.broken_timer = 50

    line = f.readline()
    star.x = int(line)
    line = f.readline()
    star.y = int(line)

    blocks.clear()
    while True:
        bx = f.readline()
        by = f.readline()
        bstate = f.readline()
        if not bx:
            break
        blocks.append(Block(int(bx), int(by), int(bstate)))

    f.close()


def enter():
    global ball, blocks, star
    ball = Ball()
    star = Star()
    blocks = []
    star.state = 1
    ball.state = 1
    load_map()

    game_world.objects = [[], [], []]

    game_world.add_object(ball, 0)
    game_world.add_object(blocks, 1)
    game_world.add_object(star, 2)



def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(mapstage_state)
            elif event.key == SDLK_RIGHT:
                ball.direction += RUN_SPEED_PPS
                ball.handle_event(RIGHT_DOWN)
            elif event.key == SDLK_LEFT:
                ball.direction -= RUN_SPEED_PPS
                ball.handle_event(LEFT_DOWN)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                ball.direction -= RUN_SPEED_PPS
                ball.handle_event(RIGHT_UP)
            elif event.key == SDLK_LEFT:
                ball.direction += RUN_SPEED_PPS
                ball.handle_event(LEFT_UP)
       #else:
       #    ball.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        if game_object == blocks:
            for block in game_object:
                block.update()
        else:
            game_object.update()


def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        if game_object == blocks:
            for block in game_object:
                block.draw()
        else:
            game_object.draw()

    update_canvas()
