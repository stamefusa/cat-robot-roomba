import pygame
from pygame.locals import *
import pygame.locals
import sys, time

def main():
    pygame.joystick.init()
    joystick0 = pygame.joystick.Joystick(0)
    joystick0.init()

    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    cur_key = ''
    pre_key = ''
    is_button_pushed = False
    
    voices =  [
        pygame.mixer.Sound("sound/output_001.wav"),
        pygame.mixer.Sound("sound/output_002.wav"),
        pygame.mixer.Sound("sound/output_003.wav"),
        pygame.mixer.Sound("sound/output_004.wav"),
        pygame.mixer.Sound("sound/output_005.wav")
    ]
    for v in voices:
        pygame.mixer.Sound.set_volume(v, 1.0)
    
    pygame.mixer.music.load("sound/bgm.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # ウィンドウの閉じるボタンが押されたとき
                pygame.joystick.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.locals.JOYBUTTONDOWN:
                is_button_pushed = True
                print(event.button)
                if event.button == 11:
                    cur_key = 'w'
                if event.button == 12:
                    cur_key = 's'
                if event.button == 13:
                    cur_key = 'a'
                if event.button == 14:
                    cur_key = 'd'
                if event.button == 6:
                    cur_key = 'z'
                if event.button == 0: # A
                    voices[0].play()
                if event.button == 1: # B
                    voices[1].play()
                if event.button == 2: # X
                    voices[2].play()
                if event.button == 3: # Y
                    voices[3].play()
                if event.button == 10: # R/ZR
                    voices[4].play()
            elif event.type == pygame.locals.JOYBUTTONUP:
                is_button_pushed = False
                cur_key = 'q' # 未入力の場合は停止扱いとする
        
        # 現在押されているキーの状態を取得
        keys = pygame.key.get_pressed()
        # 押されているキーのインデックスを取得
        pressed_keys_indices = [index for index, value in enumerate(keys) if value]

        if keys[pygame.K_ESCAPE]:
             break

        if keys[pygame.K_w]:
            cur_key = 'w'
        if keys[pygame.K_s]:
            cur_key = 's'
        if keys[pygame.K_a]:
            cur_key = 'a'
        if keys[pygame.K_d]:
            cur_key = 'd'
        if keys[pygame.K_q]:
            cur_key = 'q'
        if keys[pygame.K_z]:
            cur_key = 'z'
        if not pressed_keys_indices and not is_button_pushed:
            cur_key = 'q' # ボタンもジョイコンも未入力の場合は停止扱いとする

        # Arduinoとの通信頻度を減らすために前回入力と異なったときだけシリアルで送信
        if cur_key != pre_key:
            print(f"{time.time()}: {cur_key} is send.")
        
        # ウィンドウの背景を更新
        screen.fill((0, 0, 0))
        pygame.display.flip()

        # ループの速度を制御
        pygame.time.delay(100)

        pre_key = cur_key
    
    pygame.joystick.quit()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()