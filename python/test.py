import time
import serial

ser = serial.Serial('/dev/tty.usbserial-7D521CD33F', 115200, timeout=3)
#ser = serial.Serial('/dev/tty.usbserial-0001', 115200, timeout=3)
#time.sleep(2) 
ser.write("test3".encode())
ser.close()

""" try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().rstrip()
            print(f"Received: {data}")

        ser.write(serialCommand.encode())

        time.sleep(0.1)
except KeyboardInterrupt:
    print("terminated.")
finally:
    ser.close()
 """