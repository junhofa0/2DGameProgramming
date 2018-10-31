from pico2d import *
import random

running = True


window_width, window_height = 1000, 600
open_canvas(window_width, window_height)
hide_cursor()


ball_image = load_image("resource\\image\\ball.png")
star_image = load_image("resource\\image\\star_sheet.png")
block_thorn_image = load_image("resource\\image\\thorn_sheet.png")
block_left_image = load_image("resource\\image\\leftboost.png")
block_right_image = load_image("resource\\image\\rightboost.png")
block_jump_image = load_image("resource\\image\\jump.png")
block_basic_image = load_image("resource\\image\\block.png")
block_broken_image = load_image("resource\\image\\block_broken.png")
mouse_image = load_image("resource\\image\\mouse.png")
mouse_click_image = load_image("resource\\image\\mouse_click.png")
select_menu_image = load_image("resource\\image\\maptool_select.png")
select_image = load_image("resource\\image\\select.png")
mouse_down = False
select_x, select_y = None, None
#mouse_x, mouse_y = None, None
select_coor = {}
select_coor = {1: (845, 477), 2: (901, 477), 3: (955, 477), 4: (845, 376), 5: (901, 376), 6: (955, 376),
                   7: (845, 276), 8: (901, 276), 9: (955, 276), 0: (900, 70)}
select_x, select_y = select_coor[0]

class Ball:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 30

    def draw(self):
        global ball_image
        if (self.x != None) and (self.y != None):
            ball_image.draw(self.x, self.y)

class Star:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 40
        self.frame = 0

    def draw(self):
        global star_image
        if (self.x != None) and (self.y != None):
            star_image.clip_draw((self.frame//5) * 40, 0, 40, 40, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 40

def handle_events():
    global running
    global mouse_x
    global mouse_y
    global mouse_down
    global select_x
    global select_y
    global select_coor

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, window_height - 1 - event.y

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif (event.key >= SDLK_0) and (event.key <= SDLK_9):  # 48 <= event.key <= 57
                current_image = event.key - 48
                select_x, select_y = select_coor[current_image]

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                mouse_down = True
                mouse_x, mouse_y = event.x, window_height - 1 - event.y
                if mouse_x <= 799:
                    pass
                else:
                    pass

        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                mouse_down = False

def Draw_mouse():
    global mouse_x, mouse_y
    global mouse_down
    global mouse_image
    global mouse_click_image

    if mouse_down:
        mouse_click_image.draw(mouse_x + 18, mouse_y - 6, 40, 40)
    else:
        mouse_image.draw(mouse_x + 18, mouse_y - 6, 40, 40)

while running:
    clear_canvas()
    handle_events()

    select_menu_image.draw(900, 300)
    select_image.draw(select_x, select_y)
    Draw_mouse()

    update_canvas()

    delay(0.01)



close_canvas();
