from pico2d import *
import random

LEFT = -1
RIGHT = 1
JUMP_DOWN = 2
JUMP_UP = 3
STOP = 10   # 객체가 멈춰 있을 때(살아 있을 때)
DIE = 0     # 객체가 죽었을 때(사라졌을 때 )=> 볼과 블럭, 별의 DYING 상태가 끝난 후
DYING = 11  # 객체가 죽어가는 중 => 볼의 터지는 애이메이션, 블럭의 깨지는 애니메이션, 별의 클리어 애니메이션 상태 등

Window_width, Window_high = 800, 600
        
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
        self.col = False            # 충돌 여부 bool 변수 
        self.image = load_image('resource\\image\\ball.png')   
        self.image2 = load_image('resource\\image\\ball_bump.png')

    def draw(self):
        if self.bump == False:
            self.image.draw(self.x, self.y)
        elif self.bump == True:
            self.image2.draw(self.x, self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def jump_now(self, speed):
        self.speed = speed
        self.bump = True

    def gravitation(self):
        self.bump = False
        self.y += self.speed
        self.speed -= self.acceleration

    def bottom_collision(self):
        global blocks
        self.col = False

        for block in blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (self.y - block.y < block.r + self.r) and \
                    (block.y < self.y) and self.speed < 0:
                self.set_position(self.x, block.y + block.r + self.r)
                self.jump_now(15)
                break

    def side_collision(self):
        global blocks
        for block in blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (abs(self.y - block.y) < block.r + self.r) and \
                    abs(self.x - block.x) > abs(self.y - block.y):
                if self.direction > 0 and self.x < block.x:
                    self.set_position(block.x - block.r - self.r, self.y)
                    break
                elif self.direction < 0 and self.x > block.x:
                    self.set_position(block.x + block.r + self.r, self.y)
                    break

    def up_collision(self):
        global blocks
        for block in blocks:
            if (abs(self.x - block.x) < block.r + self.r) and (self.y < block.y) and \
                    (block.y - self.y < block.r + self.r):
                self.set_position(self.x, block.y - block.r - self.r)
                if self.speed > 0:
                    self.speed = 0
                break

    def star_col(self):
        global star
        if ((star.x - self.x) ** 2 + (star.y - self.y) ** 2) ** 0.5 <= star.r:
            star.set_state(DIE)

    def update(self):
        self.gravitation()
        self.x += self.direction * 5
        self.side_collision()
        self.bottom_collision()
        self.up_collision()

    def move_right(self):
        self.direction += RIGHT

    def move_left(self): 
        self.direction += LEFT
 
    def stop_right(self): 
        self.direction -= RIGHT
 
    def stop_left(self): 
        self.direction -= LEFT


class Star:
    def __init__(self):
        self.x = 500
        self.y = 500
        self.state = STOP
        self.r = 20
        self.frame = 0
        self.image = load_image("resource\\image\\star_sheet.png")

    def draw(self):
        if self.state != DIE:
            self.image.clip_draw((self.frame // 3) * 40, 0, 40, 40, self.x, self.y)

    def set_state(self, state):
        self.state = state

    def update(self):
        self.frame = (self.frame + 1) % 24



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
        self.frame = random.randint(0, 3)
        if self.state == 1:
            self.image = load_image("resource\\image\\block.png")
        elif self.state == 2:
            self.image = load_image("resource\\image\\block_broken.png")
        elif self.state == 3:
            self.image = load_image("resource\\image\\thorn_sheet.png")
        elif self.state == 4:
            self.image = load_image("resource\\image\\jump.png")
        elif self.state == 5:
            self.image = load_image("resource\\image\\leftboost.png")
        elif self.state == 6:
            self.image = load_image("resource\\image\\rightboost.png")

    def draw(self):
        if self.state == 3:
            self.image.clip_draw((self.frame // 6) * 40, 0, 40, 40, self.x, self.y)
        else:
            self.image.draw(self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 24


def handle_events():
    global running
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                ball.move_right()
            elif event.key == SDLK_LEFT:
                ball.move_left()
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                ball.stop_right()
            elif event.key == SDLK_LEFT:
                ball.stop_left()


open_canvas()

running = True
ball = Ball()
star = Star()
blocks = []
for i in range(20):
    blocks.append(Block(i*40, i*60, random.randint(1, 4)))

for i in range(20):
    blocks.append(Block(i*40, i*60 + 160, random.randint(1, 4)))

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
