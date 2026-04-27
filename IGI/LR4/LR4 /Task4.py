import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from abc import ABC, abstractmethod
import Input


class GeometricalFigure(ABC):
    """
    Абстрактный базовый класс для всех геометрических фигур.
    Служит интерфейсом для обеспечения наличия метода расчета площади.
    """
    @abstractmethod
    def calculate_area(self):
        """Вычисляет и возвращает площадь фигуры."""
        pass


class FigureColor:
    """
    Класс для управления цветовыми характеристиками фигуры.
    Использует механизм property для безопасного доступа к атрибуту цвета.
    """
    def __init__(self, color_name):
        """
        Инициализирует объект цвета.
        Args:
            color_name (str): Название цвета или HEX-код.
        """
        self._color = color_name

    @property
    def color(self):
        """str: Возвращает текущее название цвета."""
        return self._color

    @color.setter
    def color(self, value):
        """Устанавливает новое значение цвета."""
        self._color = value


class RegularPentagon(GeometricalFigure):
    """
    Класс, представляющий правильный пятиугольник.
    Наследуется от GeometricalFigure.
    """
    figure_name = "Правильный пятиугольник"

    def __init__(self, side, color_name):
        """
        Инициализирует пятиугольник с заданной стороной и цветом.
        Args:
            side (float): Длина стороны пятиугольника.
            color_name (str): Название цвета для отрисовки.
        Raises:
            ValueError: Если длина стороны меньше или равна нулю.
        """
        if side <= 0:
            raise ValueError("Сторона должна быть положительной")
        self.side = side
        self.color_obj = FigureColor(color_name)

    def calculate_area(self):
        """
        Рассчитывает площадь правильного пятиугольника.
        Returns:
            float: Площадь, вычисленная по формуле (5 * a^2) / (4 * tan(pi/5)).
        """
        return (5 * self.side ** 2) / (4 * math.tan(math.pi / 5))

    def get_info(self):
        """
        Формирует подробную информацию о параметрах пятиугольника.
        Returns:
            str: Отформатированная строка с названием, стороной, цветом и площадью.
        """
        info = "Название: {0}\nСторона a: {1}\nЦвет: {2}\nПлощадь: {3:.2f}".format(
            self.figure_name,
            self.side,
            self.color_obj.color,
            self.calculate_area()
        )
        return info


def draw_pentagon(pentagon, signature):
    """
    Визуализирует пятиугольник с помощью matplotlib и сохраняет результат в PNG.
    Args:
        pentagon (RegularPentagon): Объект класса пятиугольника для отрисовки.
        signature (str): Текстовая подпись, отображаемая под фигурой.
    """
    try:
        fig, ax = plt.subplots()
        a = pentagon.side

        # Визуализация через RegularPolygon
        patch = patches.RegularPolygon(
            (0, 0), numVertices=5, radius=a,
            orientation=0,
            facecolor=pentagon.color_obj.color,
            edgecolor='black'
        )

        ax.add_patch(patch)
        ax.set_xlim(-a * 1.5, a * 1.5)
        ax.set_ylim(-a * 1.5, a * 1.5)
        ax.set_aspect('equal')

        plt.text(0, -a * 1.3, signature, ha='center', fontsize=12, fontweight='bold')
        plt.title(f"Визуализация: {pentagon.figure_name}")

        plt.savefig("pentagon.png")
        plt.show()
    except Exception as e:
        print(f"Ошибка при отрисовке: {e}")


def task4():
    """
    Основная управляющая функция для Задания 4.
    Осуществляет ввод данных, создание объекта, вывод информации,
    сохранение в текстовый файл и запуск отрисовки.
    """
    print("\n--- Задание 4: Правильный пятиугольник ---")

    side = Input.get_valid_float("Введите длину стороны (a): ")
    color = Input.get_valid_color("Введите цвет (напр. 'red', 'gold', '#00FF00'): ")
    text_label = input("Введите текст подписи: ").strip()
    if not text_label: text_label = "Фигура"

    poly = RegularPentagon(side, color)
    info = poly.get_info()

    print("\n--- Параметры фигуры ---")
    print(info)

    try:
        with open("figure_info.txt", "w", encoding="utf-8") as f:
            f.write(info)
        print("Инфо сохранено в 'figure_info.txt'")
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")

    draw_pentagon(poly, text_label)
