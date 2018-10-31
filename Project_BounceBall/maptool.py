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
portal_in_image = load_image("resource\\image\\portal_in.png")
portal_out_image = load_image("resource\\image\\portal_out.png")
mouse_down = False
select_x, select_y = None, None
mouse_x, mouse_y = None, None

select_coor = {}
select_coor = {1: (845, 477), 2: (901, 477), 3: (955, 477), 4: (845, 376), 5: (901, 376), 6: (955, 376),
                   7: (845, 276), 8: (901, 276), 9: (955, 276), 0: (900, 70)}
select_x, select_y = select_coor[0]


class Block:
    x = 0
    y = 0
    size = None

    def __init__(self):
        self.frame = random.randint(0, 3)
        self.portalframe = 0
        Block.state = 0
        Block.size = 40

    def draw(self):
        global block_basic_image
        global block_thorn_image
        global block_broken_image
        global block_jump_image
        global block_left_image
        global block_right_image
        global portal_in_image
        global portal_out_image

        if self.state == 1:
            block_basic_image.draw(self.x, self.y)
        elif self.state == 2:
            block_broken_image.draw(self.x, self.y)
        elif self.state == 3:
            block_thorn_image.clip_draw((self.frame//10) * 40, 0, 40, 40, self.x, self.y)
        elif self.state == 4:
            block_jump_image.draw(self.x, self.y)
        elif self.state == 5:
            block_left_image.draw(self.x, self.y)
        elif self.state == 6:
            block_right_image.draw(self.x, self.y)
        elif self.state == 7:
            portal_in_image.clip_draw((self.portalframe//10) * 40, 0, 40, 40, self.x, self.y)
        elif self.state == 77:
            portal_out_image.clip_draw((self.portalframe // 10) * 40, 0, 40, 40, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 50
        self.portalframe = (self.portalframe + 1) % 120


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

def save_file():
    global ball
    global star
    global blocks

    fstr = input("파일저장 - 생성할 파일 이름 입력 : ")
    fname = "map\\" + fstr + ".txt"
    if os.path.exists(fname):
        answer = input("기존에 존재하는 파일이 있습니다. 덮어쓰시겠습니까? Y/N  ")
        if answer == 'y' or answer == 'Y':
            Fop = open(fname, "w")
            Fop.write(str(ball.x) + '\n')
            Fop.write(str(ball.y) + '\n')
            Fop.write(str(star.x) + '\n')
            Fop.write(str(star.y) + '\n')
            for block in blocks:
                Fop.write(str(block.x) + '\n')
                Fop.write(str(block.y) + '\n')
                Fop.write(str(block.state) + '\n')

            Fop.close()
            print("파일 덮어쓰기가 완료 되었습니다!!\n")
        elif answer == 'n' or answer == 'N':
            pass
    else:
        Fop = open(fname, "w")
        Fop.write(str(ball.x) + '\n')
        Fop.write(str(ball.y) + '\n')
        Fop.write(str(star.x) + '\n')
        Fop.write(str(star.y) + '\n')
        for block in blocks:
            Fop.write(str(block.x) + '\n')
            Fop.write(str(block.y) + '\n')
            Fop.write(str(block.state) + '\n')

        Fop.close()
        print("새로운 파일이 생성 되었습니다!!\n")

def load_file():
    global star
    global blocks
    global ball

    fstr = input("파일 불러오기 - 불러올 파일 이름 입력 : ")
    fname = "map\\" + fstr + ".txt"
    print(fname)

ball = Ball()
blocks = []
star = Star()

while running:
    clear_canvas()
    handle_events()

    select_menu_image.draw(900, 300)
    select_image.draw(select_x, select_y)
    Draw_mouse()

    update_canvas()

    delay(0.01)

close_canvas()
