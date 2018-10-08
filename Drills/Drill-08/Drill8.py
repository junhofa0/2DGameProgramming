from pico2d import *
import random

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400,30)

class Soccer_Ball:
    def __init__(self):
        self.x, self.y = random.randint(0+50, 800-50), 600
        self.speed = random.randint(700, 1500) / 100
        if random.randint(0, 1) == 1:
            self.r = 20
            self.image = load_image('ball41x41.png')
        else:
            self.r = 10
            self.image = load_image('ball21x21.png')

    def update(self):
        self.y -= self.speed
        
    def draw(self):
        self.image.draw(self.x, self.y)
        
class Boy:
    def __init__(self):
        self.x, self.y = random.randint(40, 400), 90
        self.frame = random.randint(0, 7)
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

def handle_events():

    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas()

running = True

grass = Grass()
team = [Boy() for i in range(11)]
balls = [Soccer_Ball() for i in range(20)]

while running:
    handle_events()

    for boy in team:
        boy.update()
    for ball in balls:
        ball.update()
    
    clear_canvas()
    
    grass.draw()
    for boy in team:
        boy.draw()
    for ball in balls:
        ball.draw()
        
    update_canvas()
    
    delay(0.05)
    

close_canvas()
