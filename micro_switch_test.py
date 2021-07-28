# curl -sL https://github.com/Seeed-Studio/grove.py/raw/master/install.sh | sudo bash -s -
import time
import RPi.GPIO as GPIO
www
PIN = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)

def main():
    while True:
        if GPIO.input(5) is 1:
            print("on")
        else:
            print("off")
        time.sleep(1)


if __name__ == '__main__':
    main()

