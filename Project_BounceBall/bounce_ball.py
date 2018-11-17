import random
import game_framework
import lobby_state
import main_state
import game_world
from pico2d import *

EMPTY_PLACE = 0
BASIC_BLOCK = 1
CRACKED_BLOCK = 2
THORN_BLOCK = 3
JUMP_BLOCK = 4
LEFT_BOOST_BLOCK = 5
RIGHT_BOOST_BLOCK = 6
ENTRANCE_PORTAL_BLOCK = 7
EXIT_PORTAL_BLOCK = 77

# Ball Speed
PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm = 100pixesl 1m
#RUN_SPEED_KMPH = 10.0  # Km / Hour
#RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = 1.3
RUN_SPEED_PPS = (PIXEL_PER_METER * RUN_SPEED_MPS)  # 1초에 1.3 METER = 130 PIXEL

# Ball Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

#Ball Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, DIE, BOOST_LEFT, BOOST_RIGHT, DIE_TIMER, TO_RUN = range(9)
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP
}

class RunState:
    @staticmethod
    def enter(ball, event):
        pass
    #   if event == RIGHT_DOWN:
    #       ball.velocity += 1
    #   elif event == LEFT_DOWN:
    #       ball.velocity -= 1
    #   elif event == RIGHT_UP:
    #       ball.velocity -= 1
    #   elif event == LEFT_UP:
    #       ball.velocity += 1
    #   ball.direction = clamp(-1, ball.velocity, 1)

    @staticmethod
    def exit(ball, event):
        pass

    @staticmethod
    def do(ball):
        ball.portal_col()
        ball.star_col()
        ball.side_out()
        ball.move()
        ball.gravitation()
        ball.side_collision()
        ball.bottom_collision()
        ball.up_collision()

    @staticmethod
    def draw(ball):

        if ball.bump == False:
            ball.image.draw(ball.x, ball.y)
        else:
            ball.image_bump.draw(ball.x, ball.y)

class BoostState:
    @staticmethod
    def enter(ball, event):
     #  if event == RIGHT_DOWN:
     #      ball.velocity += 1
     #  elif event == LEFT_DOWN:
     #      ball.velocity -= 1
     #  elif event == RIGHT_UP:
     #      ball.velocity -= 1
     #  elif event == LEFT_UP:
     #      ball.velocity += 1

        if event == BOOST_LEFT:
            ball.fire_speed = -RUN_SPEED_PPS * 4
        elif event == BOOST_RIGHT:
            ball.fire_speed = RUN_SPEED_PPS * 4

    @staticmethod
    def exit(ball, event):
        pass

    @staticmethod
    def do(ball):
        ball.portal_col()
        ball.star_col()
        ball.side_out()
        ball.boosting(ball.fire_speed)
        ball.boost_side_collision()

    @staticmethod
    def draw(ball):
        ball.image.draw(ball.x, ball.y)


class DieState:
    @staticmethod
    def enter(ball, event):
     #  if event == RIGHT_DOWN:
     #      ball.velocity += 1
     #  elif event == LEFT_DOWN:
     #      ball.velocity -= 1
     #  elif event == RIGHT_UP:
     #      ball.velocity -= 1
     #  elif event == LEFT_UP:
     #      ball.velocity += 1
        ball.end_timer = 0

    @staticmethod
    def exit(ball, event):
        pass

    @staticmethod
    def do(ball):
        ball.end_timer = (ball.end_timer + ACTION_PER_TIME * FRAMES_PER_ACTION * game_framework.frame_time)
        if ball.end_timer >= 8:
            #game_framework.change_state(main_state)
            ball.add_event(TO_RUN)
            main_state.start_time = get_time()
            #ball.add_event(DIE_TIMER)
            main_state.load_map()
            ball.end_timer = 0
            #game_framework.change_state(mapstage_state)

    @staticmethod
    def draw(ball):
        pass
        #ball.broken_image.clip_draw(int(ball.end_timer) * 40, 0, 40, 40, ball.die_x, ball.die_y + 5, ball.size, ball.size)


next_state_table = {
    RunState: {RIGHT_UP: RunState, LEFT_UP: RunState,
               LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
               BOOST_LEFT: BoostState, BOOST_RIGHT: BoostState,
               DIE: DieState, TO_RUN: RunState},
    BoostState: {LEFT_DOWN: BoostState, RIGHT_DOWN: BoostState,
                 LEFT_UP: BoostState, RIGHT_UP: BoostState,
                 TO_RUN: RunState, DIE: DieState},
    DieState: {LEFT_UP: DieState, RIGHT_UP: DieState,
               LEFT_DOWN: DieState, RIGHT_DOWN: DieState,
               DIE_TIMER: RunState, DIE: DieState,
                TO_RUN: RunState}
}


class Ball:
    x = None
    y = None
    velocity = None
    direction = 0

    def __init__(self):

        self.size = 30
        self.r = 15
        self.bump = False
        self.acceleration = 1260   # PIXEL / S**2  =  12.6 m/s**2
        self.basic_jump_speed = 420   # PIXEL / S  =  4.2 m/s
        self.high_jump_speed = 420 * 1.6275 # PIXEL / S  =  4.2 * 1.6275 m/s
        self.speed = 0  # 속도
        self.frame = 0
        self.die_x = 0  # 죽을 때의 위치
        self.die_y = 0  # 죽을 때의 위치
        # self.direction = 0
        self.fire_speed = RUN_SPEED_PPS * 5
        self.broken_timer = 50
        self.speed_down = 0
        self.space_time = 0
        self.end_timer = 0
        # self.velocity = 0
        self.state = 1
        self.col = False  # 부딪친 상태인지 아닌지
        self.image = load_image('resource\\image\\ball.png')
        self.image_bump = load_image('resource\\image\\ball_bump.png')
        #self.broken_image = load_image('resource\\image\\broken_ball.png')

        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            if self.cur_state == next_state_table[self.cur_state][event]:
                pass
            else:
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        # if (event.type, event.key) in key_event_table:
        #    key_event = key_event_table[(event.type, event.key)]
        #    self.add_event(key_event)
        self.add_event(event)

    def jump_now(self, speed):
        self.speed = speed
        self.bump = True

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def boosting(self, fire_speed):
        self.x = (self.x + fire_speed * game_framework.frame_time)
        main_state.start_time = get_time()

    def gravitation(self):
        self.bump = False
        self.space_time = get_time() - main_state.start_time
        self.speed_down = 1 - self.speed_down
        if self.speed_down == True:
            self.speed -= self.acceleration * self.space_time * 2
        self.y += self.speed * self.space_time
        main_state.start_time = get_time()

    def side_out(self):
        if self.y < -self.r or self.x < - 300 or self.x > 1100:
            self.die_x = self.x
            self.die_y = self.y + self.r * 2
            #self.add_event(DIE)
            self.cur_state = DieState

    def bottom_collision(self):
        self.col = False
        for block in main_state.blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (self.y - block.y < block.r + self.r - 20) and \
                    block.y < self.y and self.speed < 0 and block.state == THORN_BLOCK:  # 끝과 끝이 겹칠 때는 호출x
                self.cur_state = DieState
                self.die_x = self.x
                self.die_y = self.y
                self.col = True
                break

        for block in main_state.blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (self.y - block.y < block.r + self.r) and \
                    (block.y < self.y) and self.speed < 0 and block.state != EMPTY_PLACE:
                if (self.x <= block.x + block.r) and (self.x >= block.x - block.r):
                    if block.state == BASIC_BLOCK:
                        self.set_position(self.x, block.y + block.r + self.r)
                        self.jump_now(self.basic_jump_speed)
                        self.col = True
                    elif block.state == CRACKED_BLOCK:
                        self.set_position(self.x, block.y + block.r + self.r)
                        self.jump_now(self.basic_jump_speed)
                        block.state = 0
                        self.col = True
                    elif block.state == JUMP_BLOCK:
                        self.set_position(self.x, block.y + block.r + self.r)
                        self.jump_now(self.high_jump_speed)
                        self.col = True
                    elif block.state == LEFT_BOOST_BLOCK:
                        self.set_position(block.x - block.r - self.r, block.y + 5)
                        self.add_event(BOOST_LEFT)
                        self.col = True
                    elif block.state == RIGHT_BOOST_BLOCK:
                        self.set_position(block.x + block.r + self.r, block.y + 5)
                        self.add_event(BOOST_RIGHT)
                        self.col = True
            if self.col == True:
                break

        if self.col == False:
            for block in main_state.blocks:
                if (abs(self.x - block.x) < block.r + self.r) and (self.y - block.y < block.r + self.r) and \
                        (block.y < self.y) and self.speed < 0 and block.state != EMPTY_PLACE:
                    if (self.x > block.x + block.r) or (self.x <= block.x - block.r):
                        if block.state == BASIC_BLOCK:
                            self.set_position(self.x, block.y + block.r + self.r)
                            self.jump_now(self.basic_jump_speed)
                            self.col = True
                        elif block.state == CRACKED_BLOCK:
                            self.set_position(self.x, block.y + block.r + self.r)
                            self.jump_now(self.basic_jump_speed)
                            block.state = 0
                            self.col = True
                        elif block.state == JUMP_BLOCK:
                            self.set_position(self.x, block.y + block.r + self.r)
                            self.jump_now(self.high_jump_speed)
                            self.col = True
                        elif block.state == LEFT_BOOST_BLOCK:
                            self.set_position(block.x - block.r - self.r, block.y)
                            self.add_event(BOOST_LEFT)
                            self.col = True
                        elif block.state == RIGHT_BOOST_BLOCK:
                            self.set_position(block.x + block.r + self.r, block.y)
                            self.add_event(BOOST_RIGHT)
                            self.col = True
                            pass
                if self.col == True:
                    break

    def side_collision(self):
        for block in main_state.blocks:
            if self.direction > 0 and (abs(self.x - block.x) < block.r + self.r) and abs(self.x - block.x) > abs(
                    self.y - block.y) + 5 and (abs(self.y - block.y) < block.r + self.r) and (self.x < block.x) and \
                    block.state != EMPTY_PLACE and block.state != ENTRANCE_PORTAL_BLOCK and block.state != EXIT_PORTAL_BLOCK:

                self.set_position(block.x - block.r - self.r, self.y)
                break

            elif self.direction < 0 and (abs(self.x - block.x) < block.r + self.r) and abs(self.x - block.x) > abs(
                    self.y - block.y) + 5 and (abs(self.y - block.y) < block.r + self.r) and (self.x > block.x) and \
                    block.state != EMPTY_PLACE and block.state != ENTRANCE_PORTAL_BLOCK and block.state != EXIT_PORTAL_BLOCK:

                self.set_position(block.x + block.r + self.r, self.y)
                break

    def boost_side_collision(self):
        for block in main_state.blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (abs(self.y - block.y) < block.r + self.r) and \
                    block.state != EMPTY_PLACE and block.state != ENTRANCE_PORTAL_BLOCK and block.state != EXIT_PORTAL_BLOCK:
                if self.x > block.x:
                    self.set_position(block.x + block.r + self.r, self.y)
                elif self.x < block.x:
                    self.set_position(block.x - block.r - self.r, self.y)

                self.cur_state = RunState
                self.speed = 0

    def up_collision(self):
        for block in main_state.blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (self.y < block.y) and self.state != DIE and \
                    (block.y - self.y < block.r + self.r) and block.state != EMPTY_PLACE \
                    and block.state != ENTRANCE_PORTAL_BLOCK and block.state != EXIT_PORTAL_BLOCK:

                self.set_position(self.x, block.y - block.r - self.r)
                if self.speed > 0:
                    self.speed = 0
                break

    def star_col(self):
        if ((main_state.star.x - self.x) ** 2 + (
                main_state.star.y - self.y) ** 2) ** 0.5 <= self.r + 10 and main_state.star.state != 0:
            main_state.star.state = 0

    def portal_col(self):
        for block in main_state.blocks:
            if ((block.x - self.x) ** 2 + (
                    block.y - self.y) ** 2) ** 0.5 <= self.r and block.state == ENTRANCE_PORTAL_BLOCK:
                for portal in main_state.blocks:
                    if portal.state == EXIT_PORTAL_BLOCK:
                        self.set_position(portal.x, portal.y)
                        break
                break

    def move(self):
        self.x += self.direction * game_framework.frame_time
