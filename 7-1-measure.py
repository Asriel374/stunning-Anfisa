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
    # Создаем список для хранения результатов измерений
    measurements = []

    # Сохраняем момент начала эксперимента
    start_time = time.time()

    # Зарядка конденсатора
    GPIO.output(TROYKA_PIN, GPIO.HIGH)  # Подать 3.3В на тройка-модуль
    print("Зарядка конденсатора...")

    # Измерение напряжения во время зарядки
    while True:
        voltage = measure_voltage()
        measurements.append(voltage)
        display_on_leds(voltage)

        # Прекращаем зарядку, если напряжение достигло 97% (примерно 248 из 255)
        if voltage >= 248:
            break

    # Разрядка конденсатора
    GPIO.output(TROYKA_PIN, GPIO.LOW)  # Подать 0В на тройка-модуль
    print("Разрядка конденсатора...")

    # Измерение напряжения во время разрядки
    while True:
        voltage = measure_voltage()
        measurements.append(voltage)
        display_on_leds(voltage)

        # Прекращаем разрядку, если напряжение достигло 2% (примерно 5 из 255)
        if voltage <= 5:
            break

    # Сохраняем момент завершения эксперимента
    end_time = time.time()

    # Рассчитываем продолжительность эксперимента
    duration = end_time - start_time
    print(f"Продолжительность эксперимента: {duration:.2f} секунд")

    # Построение графика
    plt.plot(measurements)
    plt.title("Зависимость напряжения на выходе RC-цепи от номера измерения")
    plt.xlabel("Номер измерения")
    plt.ylabel("Напряжение (единицы АЦП)")
    plt.show()

    # Сохранение данных в файл data.txt
    with open("data.txt", "w") as data_file:
        for measurement in measurements:
            data_file.write(f"{measurement}\n")

    # Средняя частота дискретизации
    avg_frequency = len(measurements) / duration
    quantization_step = 3.3 / 256  # Шаг квантования АЦП

    # Сохранение настроек в файл settings.txt
    with open("settings.txt", "w") as settings_file:
        settings_file.write(f"Средняя частота дискретизации: {avg_frequency:.2f} Гц\n")
        settings_file.write(f"Шаг квантования АЦП: {quantization_step:.5f} В\n")

    # Вывод данных в терминал
    print(f"Период одного измерения: {duration / len(measurements):.5f} секунд")
    print(f"Средняя частота дискретизации: {avg_frequency:.2f} Гц")
    print(f"Шаг квантования АЦП: {quantization_step:.5f} В")

finally:
    # Подать 0 на все GPIO выходы и сбросить настройки GPIO
    GPIO.output(LED_PINS, 0)
    GPIO.cleanup()