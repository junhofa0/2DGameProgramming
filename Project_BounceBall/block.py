from pico2d import *
import game_world
import game_framework
import random

BROKING, DISAPPEAR = range(2)


BASIC_BLOCK = 1
CRACKED_BLOCK = 2
THORN_BLOCK = 3
JUMP_BLOCK = 4
LEFT_BOOST_BLOCK = 5
RIGHT_BOOST_BLOCK = 6
ENTRANCE_PORTAL_BLOCK = 7
EXIT_PORTAL_BLOCK = 77

#################################################


# Block Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class IdleState:

    @staticmethod
    def enter(block, event):
        if block.state == BASIC_BLOCK:
            block.image = load_image("resource\\image\\block.png")
        elif block.state == CRACKED_BLOCK:
            block.image = load_image("resource\\image\\block_broken.png")
        elif block.state == THORN_BLOCK:
            block.image = load_image("resource\\image\\thorn_sheet.png")
        elif block.state == JUMP_BLOCK:
            block.image = load_image("resource\\image\\jump.png")
        elif block.state == LEFT_BOOST_BLOCK:
            block.image = load_image("resource\\image\\leftboost.png")
        elif block.state == RIGHT_BOOST_BLOCK:
            block.image = load_image("resource\\image\\rightboost.png")
        elif block.state == ENTRANCE_PORTAL_BLOCK:
            block.image = load_image("resource\\image\\portal_in.png")
        elif block.state == EXIT_PORTAL_BLOCK:
            block.image = load_image("resource\\image\\portal_out.png")


    @staticmethod
    def exit(block, event):
        pass

    @staticmethod
    def do(block):
        if block.state == 3:
            block.frame = (block.frame + 2 * (FRAMES_PER_ACTION - 3) * game_framework.frame_time) % 4
        elif block.state == 7 or block.state == 77:
            block.frame = (block.frame + 1 * (FRAMES_PER_ACTION + 4) * game_framework.frame_time) % 12

        if block.state == 0:
            block.add_event(BROKING)

    @staticmethod
    def draw(block):
        if block.state == 3:
            block.image.clip_draw(int(block.frame) * 40, 0, 40, 40, block.x, block.y)
        elif block.state == 7 or block.state == 77:
            block.image.clip_draw(int(block.frame) * 40, 0, 40, 40, block.x, block.y)
        else:
            block.image.draw(block.x, block.y)


class BrokingState:

    @staticmethod
    def enter(block, event):
        #block.ani_image = load_image("resource\\image\\broken_b.png")
        block.broken_timer = 0
        block.state = 0

    @staticmethod
    def exit(block, event):
        pass

    @staticmethod
    def do(block):
        block.broken_timer = (block.broken_timer + ACTION_PER_TIME * FRAMES_PER_ACTION * game_framework.frame_time)
        if block.broken_timer >= 8:
            block.add_event(DISAPPEAR)

    @staticmethod
    def draw(block):
        pass
        #block.ani_image.clip_draw(int(block.broken_timer) * 100, 0, 100, 100, block.x, block.y)


class DieState:
    @staticmethod
    def enter(block, event):
        game_world.remove_object(block)

    @staticmethod
    def exit(block, event):
        pass

    @staticmethod
    def do(block):
        pass

    @staticmethod
    def draw(block):
        pass


next_state_table = {
    IdleState: {BROKING: BrokingState},
    BrokingState: {DISAPPEAR: DieState},
    DieState: {}
}


class Block:
    x = None
    y = None
    image = None
    state = None

    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.size = 40
        self.r = 20
        self.state = state

        if self.state == THORN_BLOCK:
            self.frame = random(0, 29)
        elif self.state == EXIT_PORTAL_BLOCK or self.state == ENTRANCE_PORTAL_BLOCK:
            self.frame = random(0, 70)

        self.event_que = []
        if self.state != 0:
            self.cur_state = IdleState
        else:
            self.cur_state = DieState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def handle_event(self, event):
        pass

    def draw(self):
        self.cur_state.draw(self)
