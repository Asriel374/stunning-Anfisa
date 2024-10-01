import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([6, 12, 5, 0, 1, 7, 11, 8], GPIO.OUT)
dac = [6, 12, 5, 0, 1, 7, 11, 8]

def double(n):
    num_str = bin(n)[2:]
    num = list(map(int, num_str))
    num = num[::-1]
    for i in range(7, len(num)-1, -1):
        num.append(0)
    return num

t = float(input())

try:
    while True:
        for i in range(256):
            GPIO.output(dac, double(i))
            time.sleep(t/512)
            GPIO.output(dac, 0)
        for i in range(255, -1, -1):
            GPIO.output(dac, double(i))
            time.sleep(t/512)
            GPIO.output(dac, 0)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()