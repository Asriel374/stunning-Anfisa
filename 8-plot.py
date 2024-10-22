import numpy as np
import matplotlib.pyplot as plt

# Чтение данных из файлов
data = np.loadtxt('data.txt')
settings = np.loadtxt('settings.txt')

# Присваивание значений из файла settings.txt
adc_values = data # Показания АЦП
sampling_frequency = settings[0]  # Средняя частота дискретизации
quantization_step = settings[1]  # Шаг квантования

# Перевод номеров отсчётов в секунды и показаний АЦП в Вольты
time = np.arange(len(data)) / sampling_frequency
voltage = data * quantization_step

# Построение графика
fig, ax = plt.subplots()
# Прорежённые маркеры
ax.plot(time, voltage, label = 'Зарядка конденсатора', color = 'b', marker = 'o', markevery = 10)

# Настройки осей
ax.set_xlim(left = 0)
ax.set_ylim(bottom = 0)

# Подписи осей
ax.set_xlabel('Время (с)')
ax.set_ylabel('Напряжение (В)')

# Название графика
ax.set_title('Зависимость напряжения от времени\nдля RC-цепи')

# Настройки сетки
ax.grid(which = 'major', linestyle = '-', linewidth = 0.75)
ax.grid(which = 'minor', linestyle = ':', linewidth = 0.5)
ax.minorticks_on()

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