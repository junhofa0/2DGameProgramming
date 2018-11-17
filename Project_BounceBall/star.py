from pico2d import *
import random
import game_world

import game_framework
import mapstage_state
import main_state

# Star Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

BROKING = range(1)

class IdleState:
    @staticmethod
    def enter(star, event):
        star.frame = 0


    @staticmethod
    def exit(star, event):
        pass

    @staticmethod
    def do(star):
        star.frame = (star.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if star.state == 0:
            star.add_event(BROKING)

    @staticmethod
    def draw(star):
        star.image.clip_draw(int(star.frame) * 40, 0, 40, 40, star.x, star.y)


class BrokingState:
    @staticmethod
    def enter(star, event):
        star.broken_timer = 0

    @staticmethod
    def exit(star, event):
        pass

    @staticmethod
    def do(star):
        star.broken_timer = (star.broken_timer + 1 * (FRAMES_PER_ACTION + 2) * game_framework.frame_time)
        if star.broken_timer >= 10:
            if int(main_state.current_play_stage) == mapstage_state.open_map_count:
                mapstage_state.open_map_count += 1
            game_framework.change_state(mapstage_state)

    @staticmethod
    def draw(star):
        pass
        #star.ani_image.clip_draw(int(star.broken_timer) * 100, 0, 100, 100, star.x, star.y + 15)


next_state_table = {
    IdleState: {BROKING: BrokingState},
    BrokingState: {},
}


class Star:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.state = 1
        self.frame = 0
        self.image = load_image("resource\\image\\star_sheet.png")
        #self.ani_image = load_image("resource\\image\\broken_s.png")
        self.event_que = []
        self.cur_state = IdleState
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

