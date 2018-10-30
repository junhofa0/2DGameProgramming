from pico2d import *
import random

running = True

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

while running:
    
