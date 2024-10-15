import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

# Настройки GPIO
DAC_PIN = [26, 19, 13, 6, 5, 11, 9, 10]  # Пины для вывода на ЦАП
LED_PIN = [21, 20, 16, 12, 7, 8, 25, 24]  # Пины для светодиодов
COMP_PIN = 4  # Пин для компаратора
TROYKA_PIN = 17  # Пин для тройка-модуля

# Инициализация GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DAC_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(COMP_PIN, GPIO.IN)
GPIO.setup(TROYKA_PIN, GPIO.OUT)

def decimal_to_binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def binary_to_dac(value):
    signal = decimal_to_binary(value)
    GPIO.output(DAC_PIN, signal)
    return value

def measure_voltage():
    for value in range(256):
        binary_to_dac(value)
        time.sleep(0.01)  # Небольшая задержка для стабилизации
        if GPIO.input(COMP_PIN) == 0:
            return value
    return 255

def display_on_leds(value):
    signal = decimal_to_binary(value)
    GPIO.output(LED_PIN, signal)

def charge_and_discharge():
    measurements = []

    try:
        # Зарядка конденсатора
        GPIO.output(TROYKA_PIN, 1)  # Подаем напряжение 3.3В
        start_time = time.time()

        while True:
            voltage = measure_voltage()
            measurements.append(voltage)
            display_on_leds(voltage)

            if voltage >= 255 * 0.97:  # 97% от максимального значения (3.3В)
                print("Конденсатор зарядился до 97%")
                break

        # Разрядка конденсатора
        GPIO.output(TROYKA_PIN, 0)  # Убираем напряжение
        print("Началась разрядка конденсатора")

        while True:
            voltage = measure_voltage()
            measurements.append(voltage)
            display_on_leds(voltage)

            if voltage <= 255 * 0.02:  # 2% от максимального значения
                print("Конденсатор разрядился до 2%")
                break

        end_time = time.time()
        duration = end_time - start_time
        print(f"Продолжительность эксперимента: {duration:.2f} секунд")

        # Сохранение данных
        with open("data.txt", "w") as data_file:
            for measurement in measurements:
                data_file.write(f"{measurement}\n")

        # График
        plt.plot(measurements)
        plt.title("Измерения напряжения на выходе RC-цепи")
        plt.xlabel("Номер измерения")
        plt.ylabel("Значение АЦП")
        plt.show()

    finally:
        GPIO.output(DAC_PIN, 0)
        GPIO.output(LED_PIN, 0)
        GPIO.cleanup()

if __name__ == "__main__":
    charge_and_discharge()