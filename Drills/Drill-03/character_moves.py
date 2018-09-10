from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

x = 400
y = 90
r =200
seta = 0
HowDirect = 1
RectOrCircle = True

clear_canvas_now()
grass.draw_now(x, 30)
character.draw_now(x, y)

while True:
    if RectOrCircle == True:
        if HowDirect == 1:
            x = x + 5
            
            if x <= 400 and x >= 0:
                if x != 400:
                    clear_canvas_now()
                    grass.draw_now(400, 30)
                    character.draw_now(x, y)
                    delay(0.01)
                else:
                    RectOrCircle = False
            else:
                if x <800 and x > 400:
                    clear_canvas_now()
                    grass.draw_now(400, 30)
                    character.draw_now(x, y)
                    delay(0.01)
                else:
                    HowDirect = 2
                    
        elif HowDirect == 2:
            y = y+5
            
            if y < 600:
                clear_canvas_now()
                grass.draw_now(400, 30)
                character.draw_now(x, y)
                delay(0.01)
            else:
                HowDirect = 3
                
        elif HowDirect == 3:
            x = x-5
            if x > 0:
                clear_canvas_now()
                grass.draw_now(400, 30)
                character.draw_now(x, y)
                delay(0.01)
            else:
                HowDirect = 4
        elif HowDirect == 4:
            if y > 90:
                y = y-5
                clear_canvas_now()
                grass.draw_now(400, 30)
                character.draw_now(x, y)
                delay(0.01)
            else:
                HowDirect = 1
                
    elif RectOrCircle == False:
        seta = seta + 0.0314
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(r*math.sin(seta + 3.14) + 400, r*math.cos(seta + 3.14) + 290)
        delay(0.01)
        if seta >= 6.28:
            seta = 0
            RectOrCircle = True
        

close_canvas()
