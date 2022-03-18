# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys

def main():
    (w,h) = (200, 400)  # 画面サイズ
    (x,y) = (200, 350)  # プレイヤー画像の初期配置座標
    pygame.init()       # pygame初期化
    pygame.display.set_mode((w, h), 0, 32)  # 画面設定
    screen = pygame.display.get_surface()

    # プレイヤー画像の取得
    player = pygame.image.load("C:\\Users\PC\Documents\python\game\sozai\cursor1.png").convert_alpha()
    rect_player = player.get_rect()
    rect_player.center = (x, y) # プレイヤー画像の初期位置

    # 背景画像（bg.jpg）の取得
    bg = pygame.image.load("C:\\Users\PC\Documents\python\game\sozai\\back.png").convert_alpha()
    rect_bg = bg.get_rect()

    while (1):
        # キーイベント処理(キャラクタ画像の移動)
        pressed_key = pygame.key.get_pressed()
        # 「←」キーが押されたらx座標を-5に移動
        if pressed_key[K_LEFT]:
            rect_player.move_ip(-5, 0)
        # 「→」キーが押されたらx座標を+5移動
        if pressed_key[K_RIGHT]:
            rect_player.move_ip(5, 0)
        # 「↑」キーが押されたらy座標を-5移動
        if pressed_key[K_UP]:
            rect_player.move_ip(0, -5)
        # 「↓」キーが押されたらy座標を+5移動
        if pressed_key[K_DOWN]:
            rect_player.move_ip(0, 5)

        pygame.display.update()     # 画面更新
        pygame.time.wait(30)        # 更新時間間隔
        screen.fill((0, 20, 0, 0))  # 画面の背景色

        # 背景画像の描画
        screen.blit(bg, rect_bg)

        # プレイヤー画像の描画
        screen.blit(player, rect_player)

        # 終了用のイベント処理
        for event in pygame.event.get():
            # マウスポインタで画像も移動
            if event.type == MOUSEMOTION:
               x, y = event.pos
               rect_player.center = (x, y)
            # 閉じるボタンが押されたとき
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # キーを押したとき
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()

main()
