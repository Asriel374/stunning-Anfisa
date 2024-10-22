import numpy as np
import matplotlib.pyplot as plt

# 1. Чтение данных из файлов data.txt и settings.txt
with open('data.txt', 'r') as data_file:
    adc_values = np.array([int(line.strip()) for line in data_file])

with open('settings.txt', 'r') as settings_file:
    settings = settings_file.readlines()
    # Извлекаем числовые значения, игнорируя единицы измерения
    sampling_frequency = float(settings[0].strip().split()[-1].replace('Гц', ''))  # Средняя частота дискретизации
    quantization_step = float(settings[1].strip().split()[-1].replace('В', ''))  # Шаг квантования АЦП

# 2. Перевод показаний АЦП в Вольты, а номера отсчётов в секунды
voltages = adc_values * quantization_step  # Перевод в Вольты
time_values = np.arange(len(adc_values)) / sampling_frequency  # Перевод номеров отсчетов в секунды

# 3. Построение графика зависимости напряжения от времени
fig, ax = plt.subplots()

# 4. Настройка линии графика: цвет, форма линии, маркеры, легенда
ax.plot(time_values, voltages, label="V(t)", color="blue", marker="o", markersize=5, markerfacecolor="red", linewidth=1)

# 5. Задание максимальных и минимальных значений для шкалы
ax.set_xlim([np.min(time_values), np.max(time_values)])
ax.set_ylim([np.min(voltages), np.max(voltages)])

# 6. Подписи осей
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")

# 7. Название графика с переносом на следующую строку
ax.set_title("Voltage across RC circuit\nCharge and Discharge", loc='center', wrap=True)

# 8. Настройка сетки (major и minor)
ax.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)
ax.minorticks_on()
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

# 9. Текст с временем зарядки и разрядки
charge_time = time_values[np.argmax(voltages)]  # Время зарядки
discharge_time = time_values[-1] - charge_time  # Время разрядки
ax.text(np.mean(time_values), np.max(voltages), f"Charge time: {charge_time:.2f}s\nDischarge time: {discharge_time:.2f}s",
        fontsize=10, color="black", ha="center", va="bottom")

# 3. Сохранение графика в файл .svg
plt.savefig('rc_circuit_graph.svg', format='svg')

# Показ графика
plt.legend()
plt.show()