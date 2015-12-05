import random
import os

from pico2d import *

import game_framework
import last_state
import start_state

name = "MainState"

hero = None
background = None
font = None

score = 0
destroyed_score = 0

BlockList = []
Block_generate_frame = 0
RightCoin_generate_frame = 0
RightCoinList = []
LeftCoin_generate_frame = 0
LeftCoinList = []

class Hero:
    image = None

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    LEFT_ATTACK, RIGHT_ATTACK, DEATH_L, DEATH_R = 0, 1, 2, 3

    def __init__(self):
        self.x, self.y = 325, 85
        self.frame = random.randint(0, 3)
        self.image_LEFT = load_image('resource\\hulk_L.png')
        self.image_RIGHT = load_image('resource\\hulk_R.png')
        self.image_DEATH = load_image('resource\\death_L.png')
        self.image_DEATH = load_image('resource\\death_R.png')
        self.state = self.LEFT_ATTACK
        self.total_frames = 0

    def handle_event(self, event):
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.state = self.LEFT_ATTACK
            self.x = 325
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.state = self.RIGHT_ATTACK
            self.x = 475

    def update(self,frame_time):
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME
        self.frame = int(self.total_frames) % 4

    #충돌체크박스
    def get_bb(self):
        return self.x -25, self.y -25, self.x +25, self.y +25

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self):
        #공격모션
        if self.state == self.LEFT_ATTACK :
            self.image_LEFT.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y)

        if self.state == self.RIGHT_ATTACK:
             self.image_RIGHT.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y)

class Background:

    def __init__(self):
        self.image = load_image('resource\\Background.png')
        self.image2 = load_image('resource\\score_back.png')
        self.image3 = load_image('resource\\destroyed_score_back.png')
        self.bgm = load_music('BackMusic.mp3')
        self.bgm.set_volume(50)
        self.bgm.repeat_play()


    def draw(self):
        self.image.draw(400, 300)
        self.image2.draw(650, 500)
        self.image3.draw(650, 450)

    def get_bb(self):
        return 0,0,799,50

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def __del__(self):
        del self.image
        del self.bgm

class Life_bar:

    img_life_bar_in = None
    img_life_bar_out = None

    def __init__(self, score):
        self.image_life_bar_out = load_image('resource\\Life_bar_Outside.png')
        self.image_life_bar_in = load_image('resource\\Life_bar_Inside.png')
        self.life = 100
        self.decreaseLife = 0.2


    def draw(self):
        self.image_life_bar_out.draw(400,500)
        #self.image_life_bar_in.draw(400,500)
        #100% 체력바 구현
        self.image_life_bar_in.clip_draw(0, 0, int(240 * (self.life / 100)) , 40, 255 + int  ( 240 * (self.life / 100) / 2), 500)


    def update(self, frame_time):
        self.life -= (frame_time * self.decreaseLife)
        self.decreaseLife += (frame_time * 2)
        if(self.decreaseLife > 10):
            self.decreaseLife = 10

        if(self.life < 0):
            self.life = 0
            gameover.draw()
            update_canvas()
            delay(1)
            #체인지스테이트로해야하는데 이건 최후의 수단임
            game_framework.change_state(last_state)
        if(self.life>100):
            self.life = 100

class Block:

    MOVE_PER_TIME = 200

    BASIC_BLOCK, LEFT_BLOCK, RIGHT_BLOCK = 0, 1, 2

    def __init__(self):
        #초기 위치
        self.x, self.y = 400, 700
        self.image_basic = load_image('resource\\block_pice.png')
        self.image_LEFT = load_image('resource\\block_L.png')
        self.image_RIGHT = load_image('resource\\block_R.png')
        self.block_num = random.randint(0,2)
        self.image_block_eff = load_image('resource\\block_eff.png')

    def draw(self):
        #블럭 3종류
        if (self.block_num == 0):
            self.image_basic.draw(self.x, self.y)

        if (self.block_num == 1):
            self.image_LEFT.draw(self.x - 32.4  ,self.y)

        if (self.block_num == 2):
            self.image_RIGHT.draw(self.x + 33.4 ,self.y)

    def get_bb(self):
         #블럭에 따른 바운딩박스
        if (self.block_num == 0):
            return  self.x -30, self.y -10, self.x +30, self.y +10
        if (self.block_num == 1):
            return  self.x - 125, self.y , self.x + 25, self.y +25
        if (self.block_num == 2 ):
            return  self.x - 25, self.y , self.x + 125, self.y +25

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def update(self,frame_time, post_block_y):
        self.y -= frame_time * self.MOVE_PER_TIME
        if(self.y < post_block_y + 50):
            self.y = post_block_y + 50

    def block_get_Y(self):
        return self.y

class Gameover:

    img_gameover = None

    def __init__(self):
        self.img_gameover = load_image('resource\\gameover.png')

    def draw(self):
        self.img_gameover.draw(400,300)

class Block_eff:

    img_block_eff = None
    block_eff_sound = None

    # 현재 6장그림을 다 보여줘야함 그게 안 됨
    # 시간개념? 프레임때문에 그런듯함

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1  / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    def __init__(self):
        self.x, self.y = 400, 90
        self.total_frames = 0
        self.img_block_eff = load_image('resource\\block_eff2.png')
        if self.block_eff_sound == None:
            self.block_eff_sound = load_wav('Music\\block_eff.wav')
            self.block_eff_sound.set_volume(90)

    def draw(self):
        self.block_eff_sound.play(1)
        #애니메이션 구현
        self.total_frames += Block_eff.FRAMES_PER_ACTION * Block_eff.ACTION_PER_TIME
        self.frame = int(self.total_frames) % 6
        self.img_block_eff.clip_draw(self.frame * 150 ,0, 150, 100 , self.x, self.y)

class RightCoin:

    img_coin = None

    def __init__(self):

        self.x, self.y = 475 , 600
        self.move_per_sec = random.randint(100, 250)
        self.img_coin = load_image('resource\\coin.png')

    def draw(self):
        self.img_coin.draw(self.x, self.y)

    def update(self,frame_time):
        self.y -= (frame_time * self.move_per_sec)

    def get_bb(self):
        return self.x -20, self.y -20, self.x +20, self.y +20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class LeftCoin:

    img_coin = None

    def __init__(self):

        self.x, self.y = 325 , 600
        self.move_per_sec = random.randint(100, 250)
        self.img_coin = load_image('resource\\coin.png')

    def draw(self):
        self.img_coin.draw(self.x, self.y)

    def update(self,frame_time):
        self.y -= (frame_time * self.move_per_sec)

    def get_bb(self):
        return self.x -20, self.y -20, self.x +20, self.y +20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

def enter():
    global hero, background, life_bar, font, gameover, block_eff

    background = Background()
    hero = Hero()
    life_bar = Life_bar(score)
    gameover = Gameover()
    block_eff = Block_eff()
    font = load_font('ENCR10B.TTF')

def exit():
    global hero, blcok, background

    del(hero)
    del(background)

def pause():
    pass

def resume():
    pass

def handle_events():
    global  hero, post_block_y, score, block_eff, destroyed_score

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                hero.handle_event(event)
                #블럭지우기
                if (BlockList[0].y < 90):
                    BlockList.pop(0)
                    block_eff.draw()
                    update_canvas()
                    score += 1
                    destroyed_score += 1
                    #건물부술시체력회복량
                    life_bar.life += 3
                else:
                    pass

            elif event.key == SDLK_LEFT:
                hero.handle_event(event)
                #블럭지우기
                if (BlockList[0].y < 90):
                    BlockList.pop(0)
                    block_eff.draw()
                    update_canvas()
                    score += 1
                    destroyed_score += 1
                    #건물부술시체력회복량
                    life_bar.life += 3
                else:
                    pass

    print(score)

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def update(frame_time):
    global BlockList, Block_generate_frame, life_bar, gameover, hero, RightCoinList, RightCoin_generate_frame, LeftCoinList, LeftCoin_generate_frame, score
    #블록들

    Block_generate_frame += frame_time
    RightCoin_generate_frame += frame_time
    LeftCoin_generate_frame += frame_time
    post_block_y = 0
    block_index = 0

    if(RightCoin_generate_frame > 0.1):
        RightCoin_generate_frame -= 0.1
        if(random.randint(0, 30) == 0):
            RightCoinList.append(RightCoin())

    if(LeftCoin_generate_frame > 0.1):
        LeftCoin_generate_frame -= 0.1
        if(random.randint(0, 30) == 0):
            LeftCoinList.append(LeftCoin())

    for block in BlockList:
        block_index += 1
        if(block_index == 1):
            block.update(frame_time, 20)
        else:
            block.update(frame_time, post_block_y)

        post_block_y = block.block_get_Y()

    for block in BlockList:
        if collide(hero, block):
            gameover.draw()
            update_canvas()
            delay(1)
            #체인지스테이트로해야하는데 이건 최후의 수단임
            game_framework.quit()

           # print('Game Over')

    for rightCoin in RightCoinList:
        rightCoin.update(frame_time)
        if collide(hero, rightCoin):
            score += 100
            life_bar.life += 10
            RightCoinList.remove(rightCoin)


    for leftCoin in LeftCoinList:
        leftCoin.update(frame_time)
        if collide(hero, leftCoin):
            # 먹고 지워야함 현재 충돌체크계속되는중
            score += 100
            life_bar.life += 10
            LeftCoinList.remove(leftCoin)

    hero.update(frame_time)
    life_bar.update(frame_time)

    if len(BlockList) < 14 and Block_generate_frame >= 0.25:
        BlockList.append(Block())
        Block_generate_frame = 0

        print(frame_time)

    delay(0.06)

def draw():
    global BlockList, RightCoinList, LeftCoinList, destroyed_score

    clear_canvas()

    background.draw()
    hero.draw()
    for block in BlockList:
        block.draw()
        #block.draw_bb()

    for rightCoin in RightCoinList:
        rightCoin.draw()

    for leftCoin in LeftCoinList:
        leftCoin.draw()

    font.draw(750, 500, '%1.f' %  score)
    font.draw(750, 450, '%1.f' % destroyed_score)
    life_bar.draw()
    #바운딩박스
    #background.draw_bb()
    #hero.draw_bb()

    update_canvas()



