import matplotlib.colors as mcolors

def number(min_val, max_val, datatype=int):
    """Универсальная проверка диапазона и типа данных."""
    while True:
        try:
            user_input = input(f"Введите число от {min_val} до {max_val}: ").strip()
            val = datatype(user_input)
            if not (min_val <= val <= max_val):
                print(f"Ошибка: число должно быть в диапазоне [{min_val}; {max_val}].")
                continue
            return val
        except ValueError:
            print(f"Ошибка: ожидается тип {datatype.__name__}.")

def get_valid_float(prompt, positive=True):
    """Проверка ввода вещественного числа."""
    while True:
        try:
            val = float(input(prompt).strip())
            if positive and val <= 0:
                print("Ошибка: значение должно быть больше нуля.")
                continue
            return val
        except ValueError:
            print("Ошибка: введите корректное число.")

def get_valid_color(prompt):
    """Проверка, понимает ли библиотека такой цвет."""
    while True:
        color = input(prompt).strip().lower()
        if mcolors.is_color_like(color):
            return color
        else:
            print(f"Ошибка: '{color}' — недопустимый цвет. Попробуйте 'red', 'blue', 'green' или HEX-код.")
