import pygame
from pygame.locals import *
import pygame.locals
import serial
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
    
    # Arduinoのシリアルポートを開く
    #ser = serial.Serial('/dev/tty.usbmodem2201', 115200)
    ser = serial.Serial('/dev/tty.AtomLite', 9600)
    time.sleep(2) # Arduinoがリセットされるのを待つ

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # ウィンドウの閉じるボタンが押されたとき
                pygame.joystick.quit()
                pygame.quit()
                ser.write('z'.encode())
                ser.close()
                sys.exit()
            elif event.type == pygame.locals.JOYBUTTONDOWN:
                is_button_pushed = True
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
            ser.write(cur_key.encode())
        
        # ウィンドウの背景を更新
        screen.fill((0, 0, 0))
        pygame.display.flip()

        # ループの速度を制御
        pygame.time.delay(100)

        pre_key = cur_key
    
    pygame.joystick.quit()
    pygame.quit()
    ser.write('z'.encode())
    ser.close()
    sys.exit()

if __name__ == '__main__':
    main()