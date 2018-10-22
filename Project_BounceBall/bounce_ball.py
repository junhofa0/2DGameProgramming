from pico2d import *

Window_width, Window_high = 800, 600
LEFT = -1
RIGHT = 1
JUMP_DOWN = 2
JUMP_UP = 3
STOP = 5

open_canvas()

class Block:
    def __init__(self):
        pass
    
class Grass: 
    def __init__(self): 
        self.x = 400
        self.y = 30
        self.image = load_image('resource\\image\\grass.png')

    def draw(self): 
        self.image.draw(self.x, self.y) 

        
class Ball:
    def __init__(self): 
        self.x = 400
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
        self.image2 = load_image('resource\\image\\bump_ball.png')

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
                
    
running = True
grass = Grass()
ball = Ball()

while running:

    clear_canvas()
    
    handle_events()
    ball.update()
    
    grass.draw()
    ball.draw()
  
    update_canvas()
    delay(0.01)
    
    
close_canvas()
