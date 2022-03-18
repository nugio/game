# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys
SCREEN = Rect(0,0,300,800)

def main():
    pygame.init()       # pygame初期化
    screen = pygame.display.set_mode(SCREEN.size)  # 画面設定

    # 各クラスにスプライトグループを割り当てる
    group = pygame.sprite.RenderUpdates()
    Player.containers = group
    Shot.containers = group
    Target.containers = group

    #各クラスの画像を読み込み
    Player.image = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\kplayer2.png").convert_alpha()
    Shot.image = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\blue.png").convert_alpha()
    Target.image = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\bubbleflog.png").convert_alpha()

    # 背景画像（bg.jpg）の取得
    bg = pygame.image.load("C:\\Users\\PC\\Documents\\python\\game\\sozai\\back.png").convert_alpha()
    rect_bg = bg.get_rect()

    clock = pygame.time.Clock()

    screen.blit(bg, rect_bg)    # 背景画像の描画
    Player()
    Target()
    pygame.display.update()

    while True:
        clock.tick(60)        # 更新時間間隔
        screen.blit(bg, rect_bg)
        group.update()
        group.draw(screen)
        pygame.display.update()     # 画面更新

        # 終了用のイベント処理
        for event in pygame.event.get():
# マウスポインタで画像も移動
#if event.type == MOUSEMOTION:
#  x, y = event.pos
# rect_player.center = (x, y)
            # 閉じるボタンが押されたとき
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # キーを押したとき
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()


class Player(pygame.sprite.Sprite):
    #"""自機"""
    speed = 5  # 移動速度
    reload_time = 15  # リロード時間
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
        # ミサイルの発射
        if pressed_keys[K_SPACE]:
            # リロード時間が0になるまで再発射できない
            if self.reload_timer > 0:
                # リロード中
                self.reload_timer -= 1
            else:
                # 発射！！！
                Shot(self.rect.center)
                self.reload_timer = self.reload_time

class Shot(pygame.sprite.Sprite):
    #"""プレイヤーが発射する弾"""
    speed = 9  # 移動速度
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
    def update(self):
        self.rect.move_ip(0, -self.speed)  # 上へ移動
        if self.rect.top < 0:  # 上端に達したら除去
            self.kill()

class Target(pygame.sprite.Sprite):
     #"""的"""
     speed = 1
     float = 1
     def __init__(self):
         pygame.sprite.Sprite.__init__(self, self.containers)
         self.rect = self.image.get_rect()
         self.rect.center = (40,50) # 初期位置
     def update(self):
         self.rect.move_ip(self.speed,-self.float)
         if self.rect.right > 300 or self.rect.left <0:  # 端に達したら跳ね返り
             self.speed = -self.speed
         if self.rect.top > 200 or self.rect.top < 20:
             self.float = -self.float

main()
