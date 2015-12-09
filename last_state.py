import game_framework
import main_state
import title_state
import start_state
from pico2d import *

#결과화면
name = "LastState"
image = None
font = None

def enter():
    global image, font
    image = load_image('resource\\last_state.png')
    font = load_font('ENCR10B.TTF')

def exit():
    global image
    del(image)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_r):
                game_framework.change_state(main_state)

def draw():
    global score, destroyed_score
    clear_canvas()
    image.draw(400, 300)
    font.draw(750, 500, '%1.f' %  score)
    font.draw(750, 450, '%1.f' % destroyed_score)
    update_canvas()
    print("결과다")

def update(frame_time):
    pass
    #global logo_time

    #if(logo_time > 1.0):
    #    logo_time = 0
    #    # game_framework.quit()
    #    game_framework.push_state(title_state)
    #delay(0.01)
    #logo_time += 0.01

def pause():
    pass

def resume():
    pass






