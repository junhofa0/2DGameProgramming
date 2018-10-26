from pico2d import *
import random

LEFT = -1
RIGHT = 1
JUMP_DOWN = 2
JUMP_UP = 3
STOP = 10
DIE = 0
DYING = 11

Window_width, Window_high = 800, 600
        
class Ball:
    def __init__(self): 
        self.x = 100
        self.y = 30
        self.size = 30
        self.r = 15
        self.bump = False
        self.acceleration = 3  # 가속도
        self.speed = 30            # 속도
        self.frame = 0
        self.Direction = 0
        self.col = False            # 충돌 여부 bool 변수 
        self.image = load_image('resource\\image\\ball.png')   
        self.image2 = load_image('resource\\image\\ball_bump.png')

    def draw(self):
        if self.bump == False:
            self.image.draw(self.x, self.y)
        elif self.bump == True:
            self.image2.draw(self.x, self.y)

    def jump(self):
        self.bump = False
        self.y += self.speed
        self.speed -= self.acceleration
        
        if self.y < 35:   
            self.y = 30
            self.speed = 28
            self.bump = True

    def bottom_collision(self):
        pass

    def side_collision(self):
        pass

    def up_collision(self):
        pass

    def star_col(self):
        pass

    def update(self):
        self.jump()
        self.x += self.Direction * 5

    def move_right(self):
        self.Direction += RIGHT

    def move_left(self): 
        self.Direction += LEFT
 
    def stop_right(self): 
        self.Direction -= RIGHT
 
    def stop_left(self): 
        self.Direction -= LEFT


class Star:
    def __init__(self):
        self.x = 500
        self.y = 500
        self.state = STOP
        self.frame = 0
        self.image = load_image("resource\\image\\star_sheet.png")

    def draw(self):
        if self.state != DIE:
            self.image.clip_draw((self.frame // 3) * 40, 0, 40, 40, self.x, self.y)

    def set_state(self, state):
        pass

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
    blocks.append(Block(i*40, i*30, random.randint(1, 4)))

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
