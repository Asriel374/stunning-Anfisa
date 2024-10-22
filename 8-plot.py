import numpy as np
import matplotlib.pyplot as plt

# Чтение данных из файлов
data = np.loadtxt('data.txt')
settings = np.loadtxt('settings.txt')

# Присваивание значений из файла settings.txt
sampling_frequency = settings[0]  # Средняя частота дискретизации
quantization_step = settings[1]  # Шаг квантования

# Перевод номеров отсчётов в секунды и показаний АЦП в Вольты
time = np.arange(len(data)) / sampling_frequency
voltage = data * quantization_step

# Построение графика
fig, ax = plt.subplots()
ax.plot(time, voltage, color='blue', marker='o', markersize=5, markerfacecolor='red', label='Напряжение на RC-цепи')

# Настройки осей
ax.set_xlim(np.min(time), np.max(time))
ax.set_ylim(np.min(voltage), np.max(voltage))

# Подписи осей
ax.set_xlabel('Время (с)')
ax.set_ylabel('Напряжение (В)')

# Название графика
ax.set_title('Зависимость напряжения от времени\nдля RC-цепи')

# Настройки сетки
ax.grid(True, which='both', linestyle='--', color='gray')

# Легенда
ax.legend()

# Текст с временем зарядки и разрядки
charge_time = time[np.argmax(voltage >= 0.97 * np.max(voltage))]
discharge_time = time[np.argmax(voltage <= 0.02 * np.max(voltage))]
ax.text(np.mean(time), np.max(voltage) * 0.9, f'Время зарядки: {charge_time:.2f} с\nВремя разрядки: {discharge_time:.2f} с', color='green')

# Сохранение графика в файл
plt.savefig('graph.svg')

# Отображение графика
plt.show()