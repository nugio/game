# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import time
import sys
import random
import math

font = 'meiryo'
sc_w = 800
sc_h = 800
SCREEN = Rect(0,0,sc_w,sc_h)
gamearea = Rect(200,0,600,800)
scorearea = Rect(0,0,200,800)

#ファイルパスの指定
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
root_path = "sozai\\"
frog_path = root_path + "bubblefrog.png"
frogitem_path = root_path + "frog.png"
obake_path = root_path + "bubbleobake.png"
obakeitem_path = root_path + "obake.png"
asiato_path = root_path + "bubbleasiato.png"
asiatoitem_path = root_path + "asiato.png"
hana_path = root_path + "bubblehana.png"
hanaitem_path = root_path + "hana.png"
sun_path = root_path + "bubblesun.png"
sunitem_path = root_path + "sun.png"
dragon_path = root_path +"dragon.png"

typedict = {0:'frog',1:'obake',2:'asiato',3:'hana',4:'sun'}
bossinit = 0

def main():
    pygame.init()       # pygame初期化
    screen = pygame.display.set_mode(SCREEN.size)  # 画面設定

    # 各クラスにスプライトグループを割り当てる
    group = pygame.sprite.RenderUpdates()
    targets_g = pygame.sprite.RenderUpdates()
    shots_g = pygame.sprite.RenderUpdates()
    boss = pygame.sprite.RenderUpdates()
    bosshit = pygame.sprite.RenderUpdates()
    frame = pygame.sprite.RenderUpdates()
    player = pygame.sprite.RenderUpdates()


    Player.containers = group,player
    Bullet.containers = group
    Task.containers = group
    Shot.containers = group,shots_g
    Target.containers = group,targets_g
    Collidebubble.containers = group
    Getitem.containers = group
    Dragon.containers = group,boss
    Dragoneye.containers = group,boss,bosshit
    Frame.containers = group,frame

    #各クラスの画像を読み込み
    Player.image = pygame.image.load(root_path + "kplayer2.png").convert_alpha()
    Shot.image = pygame.image.load(root_path + "bullet.png").convert_alpha()
    Collidebubble.image = pygame.image.load(root_path + "collidebubble.png").convert_alpha()
    Frame.image = pygame.image.load(root_path + "frame.png").convert_alpha()

    #BGMの読み込みと再生
    pygame.mixer.music.load(root_path + "\\sound\\tousindaino nitizyou.mp3")
    pygame.mixer.music.play(-1)

    #効果音の読み込み
    shot_sound = pygame.mixer.Sound(root_path + "sound\\cannon1.wav")

    # 背景画像（bg.jpg）の取得
    bg = pygame.image.load(root_path + "back.png").convert_alpha()
    rect_bg = bg.get_rect()

    clock = pygame.time.Clock()

    #フォントや固定メッセージの作成
    font1 = pygame.font.SysFont(font, 20)
    font2 = pygame.font.SysFont(font, 25)
    font3 = pygame.font.SysFont(font, 40)
    text_time = font1.render("たいむ", True, (50,50,50))
    text_get = font1.render("げっと", True, (50,50,50))
    text_task = font1.render("もくひょう", True, (50,50,50))
    text_bullet = font1.render("たま", True, (50,50,50))
    text_clear = font3.render("やったね！", True, (250,50,50))
    text_BOSS = font3.render("BOSS！", True, (250,50,50))

    encount_rate = 130  #Targetの出現率（少ないほど高い）
    Task.stagecount = 0

    Task.starttime = time.time()

    screen.blit(bg, rect_bg)    # 背景画像の描画
    myplayer = Player()
    pygame.display.update()

    for bx in range(Player.first_bullet):
        bulletapply(bx)

    for task in range(5):
        type = random.randrange(5)#0が出たとすると
        Task.taskcount[type] += 1 #[1,0,0,0,0]
        pos = (15 + task * 25, sc_h -250)
        Task.tasksprites[type].append(Task(type,pos))#[[ここにTaskスプライトが入る],[],[],[],[]]

    while True:
        clock.tick(60)        # 更新時間間隔
        screen.blit(bg, rect_bg)
        spendtime = int(time.time() - Task.starttime)

        text_timedata = font1.render(str(spendtime), True, (200,200,200))

        if Player.bullet_count == 0:
            zero_reload_time = str(math.ceil(Player.zero_reload/600*10))
            reload_view = 'たま切れ！  ' + zero_reload_time
            bullet_colour = (250,100,30)
        elif myplayer.reload_timer//10 == 0:
            reload_view = 'はっしゃOK！'
            bullet_colour = (240,160,40)
        else:
            reload_view = str(math.ceil(myplayer.reload_timer/myplayer.reload_time*3))
            bullet_colour = (250,250,250)

        text_bullet_n = font1.render(reload_view, True, bullet_colour)

        screen.blit(text_time, (5,sc_h-400))
        screen.blit(text_timedata, (20,sc_h-360))
        screen.blit(text_task, (5,sc_h-300))
        screen.blit(text_get, (5,sc_h-200))
        screen.blit(text_bullet, (5,sc_h-100))
        screen.blit(text_bullet_n, (70,sc_h-100))

        if Getitem.messagetime > 0:
            text_getitem = font2.render(Getitem.text_getitem, True, (50,200,50))
            screen.blit(text_getitem,(370,380))
            Getitem.messagetime -= 1

        if Task.stagecount == 0:
            spn = random.randrange(encount_rate)
            if spn == 0:
                if Target.targetcount < 7:
                    targetapply()

        if Task.stagecount == 1:
            if bossinit==0:
                bg = pygame.image.load(root_path + "boss.png").convert_alpha()
                rect_bg = bg.get_rect()
            bossstage()
            screen.blit(text_BOSS, (400,430))
            bosscollide(bosshit,shots_g)
            framecollide(frame,player)

        if Task.stagecount == 2:
            screen.blit(text_clear, (400,350))
            text_cleartime = font3.render("クリアタイム   " + str(Task.cleartime) + "びょう", True, (50,50,200))
            screen.blit(text_cleartime, (290,450))

        if Player.zero_reload ==0:
                bulletapply(0)
                Player.zero_reload = 600

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
                        if Player.bullet_count > 0:
                            Shot(myplayer.rect.center)
                            shot_sound.play()
                            Bullet.bullets.pop(-1).kill()
                            Player.bullet_count -= 1
                            myplayer.reload_timer = myplayer.reload_time


def bossstage():
    if Target.dragon_cnt == 0:
        targetreset()
        boss1 = Dragon(dragon_path,1,1,type)
        eye1 = Dragoneye(boss1)
        pygame.mixer.music.load(root_path + "\\sound\\GB-Action-D08-2(Boss2-Loop175).mp3")
        pygame.mixer.music.play(-1)
        Target.dragon_cnt += 1
        global bossinit
        bossinit = 1

def bosscollide(bosshit,shots_g):
    #ヒット演出入れたい
    collide_targets = pygame.sprite.groupcollide(bosshit,shots_g,False,True)
    for target in collide_targets.keys():
        target.tenmetsu = 56
        Dragon.hitcount += 1
    if Dragon.hitcount == 3:
        gameclear()

def gameclear():
    Task.stagecount =2
    Task.cleartime = int(time.time() - Task.starttime)

class Player(pygame.sprite.Sprite):
    #"""自機"""
    speed = 3  # 初期移動速度
    reload_time = 100 # リロード時間
    reload_timer = 0
    first_bullet = 7 #初期弾数
    bullet_count = 0
    zero_reload = 350 #残弾切れ時リロード時間
    stepforward = 0
    damagetime = 0

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
        self.rect.clamp_ip(gamearea)
        if self.reload_timer > 0:
            self.reload_timer -= 1
        if Player.bullet_count == 0:
            Player.zero_reload -= 1
        if Player.stepforward > 0:
            if self.rect.bottom > 500:
                self.rect.move_ip(0,-50)
                Player.stepforward = 0
        if Player.damagetime > 0:
            if self.rect.right > 700 or self.rect.left <300:
                self.speed = -self.speed
            self.rect.move_ip(self.speed*5, 0)
            Player.damagetime -=1
        else:
            self.speed = 3
        if Task.stagecount == 2:
            self.kill()

class Shot(pygame.sprite.Sprite):
    #"""プレイヤーが発射する弾"""
    speed = 6  # 移動速度
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
    def update(self):
        self.rect.move_ip(0, -self.speed)  # 上へ移動
        if self.rect.top < 0:  # 上端に達したら除去
            self.kill()

class Bullet(pygame.sprite.Sprite):
    #残弾表示
    bullets = []
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = Shot.image
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
    def update(self):
        pass

def bulletapply(bullet_count):
    pos = (15 + bullet_count * 15, sc_h -50)
    Player.bullet_count += 1
    Bullet.bullets.append(Bullet(pos))

class Task(pygame.sprite.Sprite):
    #クリア条件表示
    pathlist = [frogitem_path,obakeitem_path,asiatoitem_path,hanaitem_path,sunitem_path]
    taskcount = [0,0,0,0,0]#各Taskスプライトのカウント
    tasksprites = [[],[],[],[],[]]#各Taskスプライトを入れるリスト
    stagecount = 0
    starttime = 0
    taskcleartime = 0
    cleartime = 0
    def __init__(self,task_type,pos):
         pygame.sprite.Sprite.__init__(self, self.containers)
         self.path = Task.pathlist[task_type]
         self.image = pygame.image.load(self.path).convert_alpha()
         self.rect = self.image.get_rect()
         self.rect.center = pos
    def update(self):
        pass

def collide(shots_g,targets_g):
    #泡割れ判定
    collide_targets = pygame.sprite.groupcollide(targets_g,shots_g,True,True)
    hit_sound = pygame.mixer.Sound(root_path + "sound\\pa1.wav")

    for target in collide_targets.keys():
        Target.targetlist.remove(target)
        Collidebubble(target.rect.center)
        hit_sound.play()
        Getitem(target.type,target.rect.center)
        Target.targetcount -= 1

class Collidebubble(pygame.sprite.Sprite):
    vanishframe = 15
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
     messagetime = 0
     item_effect = ["たまのスピードアップ！（かえる）","たまがふえた！（おばけ）", \
     "いどうスピードアップ！（あしあと）","ぜんしん！（はな）","りせっと！（たいよう）"]
     text_getitem = " "

     def __init__(self,target_type,centerpos):
         pygame.sprite.Sprite.__init__(self, self.containers)
         self.path = Task.pathlist[target_type]
         self.image = pygame.image.load(self.path).convert_alpha()
         self.rect = self.image.get_rect()
         self.rect.center = centerpos # 初期位置
         Getitem.itemcount += 1
         bomb_sound = pygame.mixer.Sound(root_path + "sound\\bomb2.wav")

         #アイテム効果の獲得
         if target_type == 0:
             Shot.speed += 1
         elif target_type == 1:
             for x in range(Player.bullet_count, Player.bullet_count + 3):
                 bulletapply(x)
         elif target_type == 2:
             Player.speed +=1
         elif target_type == 3:
             Player.stepforward = 1
         elif target_type == 4:
             bomb_sound.play()
             targetreset()

         #アイテム取得メッセージ
         Getitem.text_getitem = str(Getitem.item_effect[target_type])
         Getitem.messagetime = 200

         if Task.taskcount[target_type] > 0:
             Task.tasksprites[target_type].pop(-1).kill()
             Task.taskcount[target_type] -= 1

         if Task.taskcount == [0,0,0,0,0]:
            Task.stagecount = 1
            Task.taskcleartime = int(time.time() - Task.starttime)

         #目標座標
         if Getitem.itemcount < 8:
             self.tx = -25 + Getitem.itemcount * 25
             self.ty = sc_h - 130
         else:
             self.tx = -25 + (Getitem.itemcount-7) * 25
             self.ty = sc_h - 110
         #現在座標
         self.vx = int(self.tx - self.rect.x)/30
         self.vy = int(self.ty - self.rect.y)/30

     def update(self):
         if self.rect.left >= self.tx:
             self.rect.move_ip(self.vx,0)
         if self.rect.bottom <= self.ty :
             self.rect.move_ip(0,self.vy)
         self.rect.clamp_ip(self.tx,0,sc_w - self.tx,self.ty)

         if Task.stagecount == 2:
             self.kill()

class Target(pygame.sprite.Sprite):
     #"""的"""
     targetlist=[]
     targetcount = 0
     dragon_cnt = 0
     def __init__(self,path,wspeed,vspeed,type):
         pygame.sprite.Sprite.__init__(self, self.containers)
         self.image = pygame.image.load(path).convert_alpha()
         self.rect = self.image.get_rect()
         self.x = random.randrange(230,600)
         self.y = random.randrange(50,370)
         self.rect.center = (self.x, self.y)
         self.wspeed = float(wspeed)
         self.vspeed = float(vspeed)
         self.type = type
         Target.targetcount += 1

         #移動用に現在位置をfloat値で取得
         self.flo_x = float(self.rect.x)
         self.flo_y = float(self.rect.y)

     def update(self):
         #float値の現在位置にwspeed,vspeedの値で増減させ、intに直して描画
         self.flo_x += self.wspeed
         self.flo_y += -self.vspeed

         self.rect.x = int(self.flo_x)
         self.rect.y = int(self.flo_y)

         if self.rect.right > sc_w or self.rect.left <200:  # 端に達したら跳ね返り
             self.wspeed = -self.wspeed
         if self.rect.bottom > int(sc_h*1/2) or self.rect.top < 0:
             self.vspeed = -self.vspeed

def targetapply():
    type = random.randrange(5)
    if type ==0:
        Target.targetlist.append(Target(frog_path,0.5,3,type))
    elif type ==1:
        Target.targetlist.append(Target(obake_path,2,2,type))
    elif type ==2:
        Target.targetlist.append(Target(asiato_path,3,0.5,type))
    elif type ==3:
        Target.targetlist.append(Target(hana_path,1,0.05,type))
    elif type ==4:
        Target.targetlist.append(Target(sun_path,0.05,1,type))

def targetreset():
    for target in Target.targetlist:
        target.kill()
    Target.targetlist.clear()
    Target.targetcount = 0

class Dragon (Target):
    hitcount = 0
    def __init__(self,path,wspeed,vspeed,type):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = 400
        self.y = 200
        self.rect.center = (self.x, self.y)
        self.wspeed = float(wspeed)
        self.vspeed = float(vspeed)
        self.type = type
        Target.targetcount += 1
        Dragon.hitcount = 0

        #移動用に現在位置をfloat値で取得
        self.flo_x = float(self.rect.x)
        self.flo_y = float(self.rect.y)
    def update(self):
        super().update()
        self.sp_change = random.randrange(200)
        if self.sp_change == 0:
            self.wspeed += 0.5
            if self.wspeed > 5:
                self.wspeed = 1
        elif self.sp_change == 1:
            self.wspeed -= 0.5
            if self.wspeed < -5:
                self.wspeed = -1
        elif self.sp_change == 2:
            Frame(self.rect.center)
        if Dragon.hitcount == 3:
            self.kill()

class Dragoneye(pygame.sprite.Sprite):
    tenmetsu = 0
    def __init__(self,bossname):
        self.tracetarget = bossname
        self.image1 = pygame.image.load(root_path +"dragoneye.png").convert_alpha()
        self.image2 = pygame.image.load(root_path +"blueeye.png").convert_alpha()
        self.images =[self.image1,self.image2]
        self.image = self.images[0]
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.x = bossname.rect.x + 66
        self.rect.y = bossname.rect.y + 86

    def update(self):
        if self.tenmetsu > 0:
            self.image = self.images[int(self.tenmetsu /8%2)]
            self.tenmetsu-=1
        self.rect.x = self.tracetarget.rect.x + 66
        self.rect.y = self.tracetarget.rect.y + 86
        if Dragon.hitcount == 3:
            self.kill()

class Frame(pygame.sprite.Sprite):
    #"""dragonが発射する弾"""
    speed = 5  # 移動速度
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        frame_sound = pygame.mixer.Sound(root_path + "sound\\monster1.wav")
        frame_sound.play()
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
    def update(self):
        self.rect.move_ip(0, self.speed)  # 下へ移動
        if self.rect.bottom > 800:  # 下端に達したら除去
            self.kill()

def framecollide(frame,player):
    #ヒット演出入れたい
    collide_targets = pygame.sprite.groupcollide(frame,player,True,False)
    damage_sound = pygame.mixer.Sound(root_path + "sound\\flame.wav")

    for target in collide_targets.keys():
        damage_sound.play()
        Player.damagetime = 200


main()
