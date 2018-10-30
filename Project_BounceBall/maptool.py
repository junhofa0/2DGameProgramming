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
mouse_down = False



def handle_events():
    global running
    global mouse_x
    global mouse_y
    global mouse_down

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, window_height - 1 - event.y

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
    update_canvas()

    delay(0.01)



close_canvas();
