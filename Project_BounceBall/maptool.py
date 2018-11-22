import random
import game_framework
import lobby_state

from pico2d import *

hide_cursor()
STOP = 6
DIE = 7
name = "MapTool"
select_coor = {}
select_x, select_y = None, None
ball = None
blocks = []
star = None
ball_image = None
star_image = None
block_thorn_image = None
block_left_image = None
block_right_image = None
block_jump_image = None
block_basic_image = None
block_broken_image = None
mouse_image = None
mouse_click_image = None
select_menu_image = None
select_image = None
mouse_x, mouse_y = None, None
current_image = 0
portal_blue = False
portal_yellow = False
mouse_down = False
select_bgm = None
window_width, window_height = 1000, 600

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
        self.state = STOP

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
        self.state = STOP

    def draw(self):
        global star_image
        if (self.x != None) and (self.y != None):
            star_image.clip_draw((self.frame//5) * 40, 0, 40, 40, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 40


def enter():
    global ball_image
    global star_image
    global block_thorn_image
    global block_left_image
    global block_right_image
    global block_jump_image
    global block_basic_image
    global block_broken_image
    global mouse_image
    global mouse_click_image
    global select_menu_image
    global select_image
    global portal_in_image
    global portal_out_image
    global select_coor
    global select_x, select_y
    global ball, blocks, star
    global select_bgm

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

    select_bgm = load_wav('resource\\sound\\bounceball.ogg')
    select_bgm.set_volume(70)

    select_coor = {1: (845, 477), 2: (901, 477), 3: (955, 477), 4: (845, 376), 5: (901, 376), 6: (955, 376),
                   7: (845, 276), 8: (901, 276), 9: (955, 276), 0: (900, 70)}
    select_x, select_y = select_coor[0]
    ball = Ball()
    blocks = [Block() for n in range(300)]
    star = Star()
    count = 0
    row, rank = 1, 1
    for block in blocks:
        block.x = (row - 1) * 40 + 20
        block.y = (rank - 1) * 40 + 20
        row += 1
        count += 1
        if count == 20:
            row = 1
            rank += 1
            count = 0


def exit():
    global ball_image
    global star_image
    global block_thorn_image
    global block_left_image
    global block_right_image
    global block_jump_image
    global block_basic_image
    global block_broken_image
    global mouse_image
    global mouse_click_image
    global select_menu_image
    global select_image
    global portal_in_image
    global portal_out_image
    global select_coor
    global ball, blocks, star
    global select_bgm

    del ball_image
    del star_image
    del block_thorn_image
    del block_left_image
    del block_right_image
    del block_jump_image
    del block_basic_image
    del block_broken_image
    del mouse_image
    del mouse_click_image
    del select_menu_image
    del select_image
    del portal_in_image
    del portal_out_image
    del ball
    del star
    global select_bgm

    select_coor.clear()
    blocks.clear()


def update():
    global blocks
    global star

    for block in blocks:
        block.update()
    star.update()


def draw():
    clear_canvas()

    select_menu_image.draw(900, 300)
    select_image.draw(select_x, select_y)
    for block in blocks:
        block.draw()
    ball.draw()
    Draw_mouse()
    star.draw()

    update_canvas()

def pause(): pass


def resume(): pass


def handle_events():
    global running
    global mouse_x
    global mouse_y
    global mouse_down
    global current_image
    global window_width, window_height
    global blocks
    global ball
    global star
    global portal_blue
    global portal_yellow
    global select_coor
    global f
    global select_x, select_y
    global select_bgm

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, window_height - 1 - event.y
            if mouse_x <= 799:
                if mouse_down and (current_image >= 0) and (current_image <= 6):
                    if blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state == 7:
                        blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state = 0
                        portal_blue = False
                    if blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state == 77:
                        blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state = 0
                        portal_yellow = False
                    blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state = current_image
            else:
                pass

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                lobby_state.mouse_x, lobby_state.mouse_y = mouse_x, mouse_y
                game_framework.change_state(lobby_state)
            elif (event.key >= SDLK_0) and (event.key <= SDLK_9):   # 48 <= event.key <= 57
                if current_image != event.key - 48:
                    select_bgm.play()
                current_image = event.key - 48
                select_x, select_y = select_coor[current_image]
            elif event.key == SDLK_s:
                save_file()
            elif event.key == SDLK_l:
                load_file()

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                mouse_down = True
                mouse_x, mouse_y = event.x, window_height - 1 - event.y
                if mouse_x <= 799:

                    if (current_image >= 0) and (current_image <= 6):
                        if blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state == 7:
                            blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state = 0
                            portal_blue = False
                        if blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state == 77:
                            blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state = 0
                            portal_yellow = False
                        blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state = current_image

                    elif current_image == 7:
                        if portal_blue == False:
                            current_image = 7
                            portal_blue = True
                        elif portal_blue == True:
                            if portal_yellow == True:
                                for block in blocks:
                                    if block.state == 7 or block.state == 77:
                                        block.state = 0
                                current_image = 7
                                portal_yellow = False
                            else:
                                current_image = 77
                                portal_yellow = True
                        blocks[(mouse_x // 40) + (mouse_y // 40) * 20].state = current_image

                    elif current_image == 8:
                        star.x, star.y = mouse_x, mouse_y

                    elif current_image == 9:
                        ball.x, ball.y = mouse_x, mouse_y
                else:
                    pass
            elif event.button == SDL_BUTTON_RIGHT:
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
            print("\n")
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
    if os.path.exists(fname):
        inF = open(fname, "r")

        line = inF.readline()
        ball.x = int(line)
        line = inF.readline()
        ball.y = int(line)

        line = inF.readline()
        star.x = int(line)
        line = inF.readline()
        star.y = int(line)

        for block in blocks:
            bx = inF.readline()
            by = inF.readline()
            bstate = inF.readline()
            block.x = int(bx)
            block.y = int(by)
            block.state = int(bstate)
        inF.close()
        print("해당 파일을 불러 왔습니다..\n")
    else:
        print("해당 파일이 존재하지 않습니다.\n")
