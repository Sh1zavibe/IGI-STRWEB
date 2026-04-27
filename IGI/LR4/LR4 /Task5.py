import numpy as np


def task5():
    print("--- Задание 5: Работа с NumPy ---")

    # 1. Формирование матрицы A[n, m]
    try:
        n = int(input("Введите количество строк (n): "))
        m = int(input("Введите количество столбцов (m): "))
    except ValueError:
        print("Ошибка ввода. Используем значения по умолчанию 5x5.")
        n, m = 5, 5

    # Создание целочисленной матрицы случайных чисел от 1 до 100
    matrix_a = np.random.randint(1, 101, size=(n, m))

    print("\nИсходная матрица A:")
    print(matrix_a)

    # 1. Создание из списка
    sample_list = [1, 2, 3]
    np_arr = np.array(sample_list)

    # 2. Функции создания массивов заданного вида
    zeros_arr = np.zeros((2, 2))  # Матрица нулей
    ones_arr = np.ones((2, 2))  # Матрица единиц
    eye_arr = np.eye(3)  # Единичная матрица

    # 3. Индексирование и срезы
    # Пример: вторая строка, элементы со второго по третий
    slice_example = matrix_a[1, 1:3]

    # 4. Универсальные функции (ufunc)
    sqrt_matrix = np.sqrt(matrix_a)  # Поэлементное извлечение корня

    # Для статистики возьмем всю матрицу
    print(f"\nСтатистика по всей матрице:")
    print(f"Среднее (mean): {np.mean(matrix_a):.2f}")
    print(f"Медиана (median): {np.median(matrix_a):.2f}")
    print(f"Стандартное отклонение (std): {np.std(matrix_a):.2f}")

    # Корреляция (между первыми двумя строками, если их > 1)
    if n > 1:
        corr = np.corrcoef(matrix_a[0, :], matrix_a[1, :])[0, 1]
        print(f"Корреляция между 1-й и 2-й строками: {corr:.2f}")

    # 1. Получение элементов побочной диагонали
    # Побочная диагональ в матрице n x m — это элементы A[i, m - 1 - i]
    # Мы можем использовать np.fliplr (переворот слева направо) и взять главную диагональ
    side_diag = np.diag(np.fliplr(matrix_a))

    print(f"\nЭлементы побочной диагонали: {side_diag}")

    # 2. Наименьший элемент на побочной диагонали
    min_element = np.min(side_diag)
    print(f"Наименьший элемент побочной диагонали: {min_element}")

    # 3. Вычисление дисперсии двумя способами

    # Способ 1: Стандартная функция var()
    var_builtin = np.var(side_diag)

    # Способ 2: Программирование формулы
    # Формула: Var = sum((x - mean)^2) / N
    mean_diag = np.mean(side_diag)
    var_manual = np.sum((side_diag - mean_diag) ** 2) / len(side_diag)

    print(f"\nДисперсия побочной диагонали (функция NumPy): {var_builtin:.2f}")
    print(f"Дисперсия побочной диагонали (по формуле): {var_manual:.2f}")
