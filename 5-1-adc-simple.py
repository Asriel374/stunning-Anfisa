import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal12binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for value in range(256):
        signal = decimal12binary(value)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        if GPIO.input(comp) == 1:
            return value
    return 255

try:
    while True:
        value = adc()
        voltage = value / 255 * 3.3
        print("Digital value: {}, Voltage: {:.2f}V".format(value, voltage))
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()