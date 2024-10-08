import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal12binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    value = 0
    for i in range(8):
        step = 2**(7 - i)
        signal = decimal12binary(value + step)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        if GPIO.input(comp) == 0:
            value += step
    return value
    
def display(value):
    signal = decimal12binary(value)
    GPIO.output(led, signal)

try:
    while True:
        value = adc()
        voltage = value / 255 * 3.3
        display(value)
        print("Digital value: {}, Voltage: {:.2f}V".format(value, voltage))
finally:
    GPIO.output(dac, 0)
    GPIO.output(led, 0)
    GPIO.cleanup()