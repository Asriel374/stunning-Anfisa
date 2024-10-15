import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

LED_PINS = [2, 3, 4, 17, 27, 22, 10, 9]  
DAC_PINS = [8, 11, 7, 1, 0, 5, 12, 6]  
COMP_PIN = 14  
TROYKA_PIN = 13  

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PINS, GPIO.OUT)
GPIO.setup(DAC_PINS, GPIO.OUT)
GPIO.setup(COMP_PIN, GPIO.IN)
GPIO.setup(TROYKA_PIN, GPIO.OUT)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def measure_voltage():
    for value in range(256):
        GPIO.output(DAC_PINS, dec2bin(value))
        time.sleep(0.001)  
        if GPIO.input(COMP_PIN) == 0:
            return value
    return 255  

def display_on_leds(value):
    GPIO.output(LED_PINS, dec2bin(value))

try:
    measurements = []

    start_time = time.time()

    GPIO.output(TROYKA_PIN, GPIO.HIGH)  
    print("Зарядка конденсатора...")

    while True:
        voltage = measure_voltage()
        measurements.append(voltage)
        display_on_leds(voltage)

        if voltage >= 248:
            break

    GPIO.output(TROYKA_PIN, GPIO.LOW)  
    print("Разрядка конденсатора...")

    while True:
        voltage = measure_voltage()
        measurements.append(voltage)
        display_on_leds(voltage)

        if voltage <= 5:
            break

    end_time = time.time()

    duration = end_time - start_time
    print(f"Продолжительность эксперимента: {duration:.2f} секунд")

    plt.plot(measurements)
    plt.title("Зависимость напряжения на выходе RC-цепи от номера измерения")
    plt.xlabel("Номер измерения")
    plt.ylabel("Напряжение (единицы АЦП)")
    plt.show()

    with open("data.txt", "w") as data_file:
        for measurement in measurements:
            data_file.write(f"{measurement}\n")

    avg_frequency = len(measurements) / duration
    quantization_step = 3.3 / 256  # Шаг квантования АЦП

    with open("settings.txt", "w") as settings_file:
        settings_file.write(f"Средняя частота дискретизации: {avg_frequency:.2f} Гц\n")
        settings_file.write(f"Шаг квантования АЦП: {quantization_step:.5f} В\n")

    print(f"Период одного измерения: {duration / len(measurements):.5f} секунд")
    print(f"Средняя частота дискретизации: {avg_frequency:.2f} Гц")
    print(f"Шаг квантования АЦП: {quantization_step:.5f} В")

finally:
    GPIO.output(LED_PINS, 0)
    GPIO.cleanup()