import RPi.GPIO as GPIO
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
def decimal_to_binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]
try:
    while True:
        value = int(input())
        if value == 'q':
            break
        if value < 0 or value > 255:
            print()
            continue
        binary_value = decimal_to_binary(value)
        GPIO.output(dac, binary_value)
        voltage = value / 255 * 3.3
except ValueError:
    print('Ошибка: введите целое число')
except KeyboardInterrupt:
    print('Программа прервана из-за клавиатуры, не трогай!')
finally:
    GPIO.out(dac,[0, 0])
    GPIO.cleanup()
    #прога всё!