from pico2d import *
import game_framework
import game_world
import mapstage_state
import pause_state

import bounce_ball
from block import Block
from star import Star

# Ball Speed
PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm = 100pixel 1m
RUN_SPEED_MPS = 1.3
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # 1초에 1.3 METER = 130 PIXEL


name = "MainState"

ball = None
blocks = []
star = None
current_play_stage = ''
start_time = None
background_image = None

def load_map():

    global ball
    global star
    global blocks
    global current_play_stage

    #Ball.x = 0
    #Ball.y = 0

    fname = "map\\map" + current_play_stage + ".txt"
    f = open(fname, 'r')

    line = f.readline()
    ball.x = int(line)
    line = f.readline()
    ball.y = int(line)

    ball.handle = True
    ball.boost = False
    ball.broken_timer = 50
    ball.end_timer = 0

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
    global ball, blocks, star, start_time
    global background_image

    background_image = load_image('resource\\image\\ingame_background.png')

    ball = bounce_ball.Ball()
    star = Star()
    blocks = []
    star.state = 1
    ball.state = 1
    #ball.direction = mapstage_state.dire * RUN_SPEED_PPS
    load_map()

    game_world.objects = [[], [], []]
    game_world.add_object(ball, 0)
    game_world.add_object(blocks, 1)
    game_world.add_object(star, 2)

    start_time = get_time()



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
                bounce_ball.Ball.direction += RUN_SPEED_PPS
                ball.handle_event(bounce_ball.RIGHT_DOWN)
            elif event.key == SDLK_LEFT:
                bounce_ball.Ball.direction -= RUN_SPEED_PPS
                ball.handle_event(bounce_ball.LEFT_DOWN)
            elif event.key == SDLK_p:
                game_framework.push_state(pause_state)
            elif event.key == SDLK_r:
                load_map()
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                bounce_ball.Ball.direction -= RUN_SPEED_PPS
                ball.handle_event(bounce_ball.RIGHT_UP)
            elif event.key == SDLK_LEFT:
                bounce_ball.Ball.direction += RUN_SPEED_PPS
                ball.handle_event(bounce_ball.LEFT_UP)


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

