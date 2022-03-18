# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys
import random
SCREEN = Rect(0,0,300,800)

def main():
    pygame.init()       # pygame初期化
    screen = pygame.display.set_mode(SCREEN.size)  # 画面設定

    # 各クラスにスプライトグループを割り当てる
    group = pygame.sprite.RenderUpdates()
    targets_g = pygame.sprite.RenderUpdates()
    shots_g = pygame.sprite.RenderUpdates()
    Player.containers = group
    Shot.containers = group,shots_g
    Target.containers = group,targets_g
    Collidebubble.containers = group
    Getitem.containers = group

    #各クラスの画像を読み込み
    Player.image = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\kplayer2.png").convert_alpha()
    Shot.image = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\blue.png").convert_alpha()
    Target.image = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\bubbleflog.png").convert_alpha()
    Collidebubble.image = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\collidebubble.png").convert_alpha()
    Getitem.image = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\frog.png").convert_alpha()


    # 背景画像（bg.jpg）の取得
    bg = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\back.png").convert_alpha()
    rect_bg = bg.get_rect()

    clock = pygame.time.Clock()
    encount_rate = 150  #Targetの出現率（少ないほど高い）

    screen.blit(bg, rect_bg)    # 背景画像の描画
    myplayer = Player()
    Target()
    pygame.display.update()

    while True:
        clock.tick(60)        # 更新時間間隔
        screen.blit(bg, rect_bg)

        spn = random.randrange(encount_rate)
        if spn == 0:
            if Target.targetcount < 5:
                Target()

        group.update()
        collide(shots_g,targets_g)
        group.draw(screen)
        pygame.display.update()     # 画面更新

        # 終了用のイベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # キーを押したとき
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    if myplayer.reload_timer == 0:
                        Shot(myplayer.rect.center)
                        myplayer.reload_timer = myplayer.reload_time


class Player(pygame.sprite.Sprite):
    #"""自機"""
    speed = 5  # 移動速度
    reload_time = 15  # リロード時間
    reload_timer = 0
    def __init__(self):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN.bottom # 初期位置
        self.reload_timer = 0
    def update(self):
        # 押されているキーをチェック
        pressed_keys = pygame.key.get_pressed()
        # 押されているキーに応じてプレイヤーを移動
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        self.rect.clamp_ip(SCREEN)
        if self.reload_timer > 0:
            self.reload_timer -= 1

class Shot(pygame.sprite.Sprite):
    #"""プレイヤーが発射する弾"""
    speed = 10  # 移動速度
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
    def update(self):
        self.rect.move_ip(0, -self.speed)  # 上へ移動
        if self.rect.top < 0:  # 上端に達したら除去
            self.kill()

def collide(shots_g,targets_g):
    #泡割れ判定
    collide_targets = pygame.sprite.groupcollide(shots_g,targets_g,True,True)
    for target in collide_targets.keys():
        Collidebubble(target.rect.center)
        Getitem(target.rect.center)
        Target.targetcount -= 1


class Collidebubble(pygame.sprite.Sprite):
    vanishframe = 30
    def __init__(self,centerpos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = centerpos
    def update(self):
        self.vanishframe -= 1
        if self.vanishframe == 0:
            self.kill()

class Getitem(pygame.sprite.Sprite):
     #"""倒したターゲットをアイテム化"""
     itemcount = 0
     def __init__(self,centerpos):
         pygame.sprite.Sprite.__init__(self, self.containers)
         self.rect = self.image.get_rect()
         self.rect.center = centerpos # 初期位置
         Getitem.itemcount += 1
     def update(self):
         tx = 290
         ty = 780 - Getitem.itemcount*40
         if self.rect.right < tx:
             self.rect.move_ip(2,0)
         if self.rect.bottom < ty :
             self.rect.move_ip(0,4)

class Target(pygame.sprite.Sprite):
     #"""的"""
     speed = 1
     float = 1
     targetcount = 0
     def __init__(self):
         pygame.sprite.Sprite.__init__(self, self.containers)
         self.rect = self.image.get_rect()
         self.rect.center = (40,50) # 初期位置
         Target.targetcount += 1
     def update(self):
         self.rect.move_ip(self.speed,-self.float)
         if self.rect.right > 300 or self.rect.left <0:  # 端に達したら跳ね返り
             self.speed = -self.speed
         if self.rect.top > 200 or self.rect.top < 20:
             self.float = -self.float

main()
