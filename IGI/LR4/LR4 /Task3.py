import math
import statistics
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


class CosApproximation:
    def __init__(self, eps):
        self.eps = eps
        self.history = []
    def calculate_single(self, x):
        """Вычисляет cos(x) для конкретного x и возвращает данные и список всех членов ряда."""
        max_iter = 500
        term = 1.0
        sum_series = 0.0
        n = 0
        terms_list = []

        while n < max_iter:
            terms_list.append(term)
            sum_series += term
            if abs(term) < self.eps:
                break

            n += 1
            multiplier = -(x ** 2) / ((2 * n - 1) * (2 * n))
            term *= multiplier
        else:
            print(f"Внимание: точность {self.eps} не достигнута за {max_iter} итераций.")

        exact = math.cos(x)
        res = [x, n + 1, sum_series, exact, self.eps]
        self.history.append(res)
        return res, terms_list

    def get_statistics(self, sequence):
        """Вычисляет статистические параметры последовательности членов ряда."""
        if not sequence:
            return None

        mean_val = statistics.mean(sequence)
        median_val = statistics.median(sequence)
        try:
            mode_val = statistics.mode(sequence)
        except statistics.StatisticsError:
            mode_val = sequence[0]

        variance_val = statistics.variance(sequence) if len(sequence) > 1 else 0
        stdev_val = statistics.stdev(sequence) if len(sequence) > 1 else 0

        return {
            "Среднее": mean_val,
            "Медиана": median_val,
            "Мода": mode_val,
            "Дисперсия": variance_val,
            "СКО": stdev_val
        }

    def plot_results(self):
        """Рисует графики и сохраняет в файл."""
        # Генерируем значения x для плавного графика
        x_plot = np.linspace(-2 * np.pi, 2 * np.pi, 500)
        y_math = [math.cos(i) for i in x_plot]
        y_series = [self.calculate_single(i)[0][2] for i in x_plot]

        plt.figure(figsize=(10, 6))
        plt.plot(x_plot, y_math, label='math.cos(x)', color='blue', linewidth=2)
        plt.plot(x_plot, y_series, '--', label='Maclaurin Series', color='red', linewidth=2)

        # Оформление
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.title(f"Сравнение функций (eps={self.eps})")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True, linestyle=':')

        # Сохранение
        plt.savefig("cos_plot.png")
        print("\nГрафик сохранен как 'cos_plot.png'")
        plt.show()


def task3():
    print("--- Задание 3: Ряд Маклорена для Cos(x) ---")
    x_val = float(input("Введите x (например, 1.0): "))
    eps_val = float(input("Введите точность (например, 0.0001): "))

    # 1. Создание объекта класса
    calculator = CosApproximation(eps_val)

    # 2. Расчет
    result_row, terms = calculator.calculate_single(x_val)

    # 3. Вывод таблицы (пункт а)
    headers = ["x", "n", "F(x)", "Math F(x)", "eps"]
    print("\nРезультаты расчета:")
    print(tabulate([result_row], headers=headers, tablefmt="grid"))

    # 4. Вывод статистики (пункт а - дополнительные параметры)
    stats = calculator.get_statistics(terms)
    print("\nСтатистика последовательности членов ряда:")
    for key, val in stats.items():
        print(f"{key}: {val:.6f}")

    # 5. Построение графиков (пункты б, в)
    calculator.plot_results()