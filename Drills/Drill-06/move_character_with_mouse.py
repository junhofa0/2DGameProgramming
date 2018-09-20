from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

# 최종완성

def handle_events():
    global mx, my      # 마우스 좌표
    global gx, gy      # 클릭한 좌표 ( 캐릭터가 도착해야하는 좌표 )
    global sx, sy      # 시작 좌표 ( 캐릭터의 시작 좌표 )
    global x, y        # 현재 캐릭터의 좌표
    global click
    global count
    global running
    events = get_events()
    
    for event in events:
        if event.type == SDL_MOUSEBUTTONDOWN:
            gx, gy = event.x , KPU_HEIGHT - 1 - event.y
            sx, sy = x, y
            count = 30
            click = True
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_QUIT:
            running = False

open_canvas(KPU_WIDTH, KPU_HEIGHT)  

MouseIcon = load_image('hand_arrow.png')
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')

x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
running = True
click = False
mx, my = 0, 0
gx, gy = 0, 0
sx, sy = 0, 0
count = 30
direc = 1
frame = 0
hide_cursor()


while running:
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)

    if click == True:

        if gx - sx > 0:
            direc = 1
        elif gx - sx < 0:
            direc = -1

        x += (gx - sx) / 30
        y += (gy - sy) / 30

        count -= 1

        if count == 0:
            click = False

    if direc == 1:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    elif direc == -1:
        character.clip_draw(frame * 100, 100 * 0, 100, 100, x, y)
    MouseIcon.draw(mx + 25, my-25)
    update_canvas()
    
    frame = (frame + 1) % 8

    delay(0.02)
    handle_events()

close_canvas()