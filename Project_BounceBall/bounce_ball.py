import random
import game_framework
import lobby_state
import main_state
import game_world
from pico2d import *

#from block import*
#from star import*

# Ball Speed
PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm = 100pixel 1m
#RUN_SPEED_KMPH = 10.0  # Km / Hour
#RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = 1.5
RUN_SPEED_PPS = (PIXEL_PER_METER * RUN_SPEED_MPS)  # 1초에 1.5 METER = 150 PIXEL

# Ball Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
        
class Ball:
    def __init__(self): 
        self.x = 100
        self.y = 200
        self.size = 30
        self.r = 15
        self.bump = False
        self.acceleration = 1.5  # 가속도
        self.speed = 15            # 속도
        self.frame = 0
        self.direction = 0
        self.state = STOP
        self.col = False            # 충돌 여부 bool 변수 
        self.image = load_image('resource\\image\\ball.png')   
        self.image2 = load_image('resource\\image\\ball_bump.png')

    def draw(self):
        if self.state != DIE:
            if self.bump == False:
                self.image.draw(self.x, self.y)
            elif self.bump == True:
                self.image2.draw(self.x, self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_state(self, state):
        self.state = state

    def jump_now(self, speed):
        self.speed = speed
        self.bump = True

    def gravitation(self):
        self.bump = False
        self.y += self.speed
        self.speed -= self.acceleration

    def boosting(self, fire_speed):
        if self.state == LEFT_BOOST:
            self.x -= fire_speed
        elif self.state == RIGHT_BOOST:
            self.x += fire_speed

    def bottom_collision(self):
        global blocks
        self.col = False

        for block in blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (self.y - block.y < block.r + self.r - 20) and \
                    block.y < self.y and self.state != DIE and self.state != DYING and self.speed < 0 and block.state == 3:  # 끝과 끝이 겹칠 때는 호출x
                self.set_state(DIE)
                break

        for block in blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (self.y - block.y < block.r + self.r) and \
                    (block.y < self.y) and self.speed < 0:
                if (self.x <= block.x + block.r) and (self.x >= block.x - block.r) and block.state != DIE:
                    if block.state == 1:
                        self.set_position(self.x, block.y + block.r + self.r)
                        self.jump_now(15)
                        self.col = True
                    elif block.state == 2:
                        self.set_position(self.x, block.y + block.r + self.r)
                        self.jump_now(15)
                        block.state = DIE
                        self.col = True
                    elif block.state == 4:
                        self.set_position(self.x, block.y + block.r + self.r)
                        self.jump_now(25)
                        self.col = True
                    elif block.state == 5:
                        self.set_position(block.x - block.r - self.r, block.y)
                        self.set_boosting(LEFT_BOOST, 10)
                        self.col = True
                    elif block.state == 6:
                        self.set_position(block.x + block.r + self.r, block.y)
                        self.set_boosting(RIGHT_BOOST, 10)
                        self.col = True
            if self.col == True:
                break

        if self.col == False:
            for block in blocks:
                if (abs(self.x - block.x) < block.r + self.r) and (self.y - block.y < block.r + self.r) and \
                        (block.y < self.y) and self.speed < 0 and self.state != DIE and self.state != DYING and block.state != DYING:
                    if ((self.x > block.x + block.r) or (self.x <= block.x - block.r)) and block.state != DIE:
                        if block.state == 1:
                            self.set_position(self.x, block.y + block.r + self.r)
                            self.jump_now(15)
                            self.col = True
                        elif block.state == 2:
                            self.set_position(self.x, block.y + block.r + self.r)
                            self.jump_now(15)
                            block.state = DYING  ####
                            self.col = True
                        elif block.state == 4:
                            self.set_position(self.x, block.y + block.r + self.r)
                            self.jump_now(12.5)
                            self.col = True
                        elif block.state == 5:
                            self.set_position(block.x - block.r - self.r, block.y)
                            self.set_boosting(LEFT_BOOST, 18)
                            self.col = True
                        elif block.state == 6:
                            self.set_position(block.x + block.r + self.r, block.y)
                            self.set_boosting(RIGHT_BOOST, 18)
                            self.col = True
                if self.col == True:
                    break
            

    def side_collision(self):
        global blocks
        for block in blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (abs(self.y - block.y) < block.r + self.r) and \
                    abs(self.x - block.x) > abs(self.y - block.y) and block.state != DYING and \
                block.state != DIE and self.state != DIE and self.state != DYING:
                if self.direction > 0 and self.x < block.x:
                    self.set_position(block.x - block.r - self.r, self.y)
                    break
                elif self.direction < 0 and self.x > block.x:
                    self.set_position(block.x + block.r + self.r, self.y)
                    break

    def boost_side_collision(self):
        global blocks
        for block in blocks:
            if self.state != DIE and (abs(self.x - block.x) < block.r + self.r) and (
                    abs(self.y - block.y) < block.r + self.r) and \
                    block.state != DIE and block.state != DYING and block.state != 7 and block.state != 77 and self.state != DYING:

                self.speed = 0
                self.set_state(STOP)

                if self.x > block.x:
                    self.set_position(block.x + block.r + self.r, self.y)
                elif self.x < block.x:
                    self.set_position(block.x - block.r - self.r, self.y)

    def up_collision(self):
        global blocks
        for block in blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (self.y < block.y) and \
                    (block.y - self.y < block.r + self.r) and self.state != DIE and block.state != DYING and \
                    block.state != DIE and self.state != DYING:
                self.set_position(self.x, block.y - block.r - self.r)
                if self.speed > 0:
                    self.speed = 0
                break

    def star_col(self):
        global star
        if ((star.x - self.x) ** 2 + (star.y - self.y) ** 2) ** 0.5 <= star.r:
            star.set_state(DIE)

    def update(self):
        if self.state == LEFT_BOOST or self.state == RIGHT_BOOST:
            self.boosting(self.fire_speed)
            self.side_collision()
            self.boost_side_collision()
        else:
            if self.state != DIE and self.state != DYING:
                self.move()
                self.gravitation()
                if self.direction != 0:
                    self.side_collision()
        self.bottom_collision()
        self.up_collision()
        self.star_col()

    def move(self):
        self.x += self.direction * 3

    def move_right(self):
        self.direction += RIGHT

    def move_left(self): 
        self.direction += LEFT
 
    def stop_right(self): 
        self.direction -= RIGHT
 
    def stop_left(self): 
        self.direction -= LEFT


open_canvas()

running = True
ball = Ball()
star = Star()
blocks = []
for i in range(20):
    blocks.append(Block(i*40, i*40, random.randint(1, 4)))

for i in range(20):
    blocks.append(Block(i*40, i*40 + 160, random.randint(1, 4)))

while running:
    handle_events()
    clear_canvas()

    star.update()
    for block in blocks:
        block.update()
    ball.update()

    star.draw()
    for block in blocks:
        block.draw()
    ball.draw()

    update_canvas()
    delay(0.01)

close_canvas()
