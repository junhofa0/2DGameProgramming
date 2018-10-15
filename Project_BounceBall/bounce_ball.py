from pico2d import *

Window_width, Window_high = 800, 600
LEFT = -1
RIGHT = 1
JUMP_DOWN = 2
JUMP_UP = 3
STOP = 5

open_canvas()

class block:
    def __init__(self):
        pass

class Grass:
    def __init__(self): 
        self.x = 400
        self.y = 30
        self.image = load_image('grass.png')

class Ball:
    def __init__(self): 
        self.x = 400
        self.y = 30
        self.bump = False
        self.acceleration = 3  # 가속도
        self.speed = 30            # 속도
        self.frame = 0
        self.Direction = 0
        self.image = load_image('resource\\image\\ball.png')   
        self.image2 = load_image('resource\\image\\bump_ball.png')

running = True
grass = Grass()
ball = Ball()
