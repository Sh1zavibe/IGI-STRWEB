import pandas as pd
import numpy as np


def task6():
    print("--- Задание 6: Исследование Pandas (Netflix Stock) ---")

    file_path = "NFLX.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден. Генерируем тестовые данные...")
        data = {
            'Date': pd.date_range(start='2020-01-01', periods=100),
            'Close': np.random.uniform(300, 600, 100),
            'Volume': np.random.randint(1000000, 5000000, 100)
        }
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)

    # 1. Из столбца Volume создаем Series
    volume_series = df['Volume']

    print("\nПервые 5 элементов volume_series:")
    print(volume_series.head())

    # 3. Доступ к элементам через .iloc (по индексу) и .loc (по метке)
    print(f"\nЭлемент по индексу 0 (.iloc): {volume_series.iloc[0]}")
    print(f"Элемент по метке 0 (.loc): {volume_series.loc[0]}")

    # 4. Средний объем (агрегация)
    avg_total_volume = volume_series.mean()
    print(f"\nСредний объем торгов (общий): {avg_total_volume:.2f}")

    print("\n--- Информация о датафрейме ---")
    df.info()  # Выводит типы данных и пропуски
    print("\nОсновные статистики:")
    print(df.describe())

    # Расчет квантилей (процентилей) для цены закрытия
    q_high = df['Close'].quantile(0.95)
    q_low = df['Close'].quantile(0.05)

    print(f"\n95% процентиль (порог роста): {q_high:.2f}")
    print(f"5% процентиль (порог падения): {q_low:.2f}")

    # Фильтрация данных
    # Дни с максимальным ростом (Close > 95% процентиля)
    high_growth_days = df[df['Close'] > q_high]
    # Дни с максимальным падением (Close < 5% процентиля)
    max_drop_days = df[df['Close'] < q_low]

    # Средние объемы для этих групп
    avg_vol_high = high_growth_days['Volume'].mean()
    avg_vol_low = max_drop_days['Volume'].mean()

    print(f"Средний объем в дни роста: {avg_vol_high:.2f}")
    print(f"Средний объем в дни падения: {avg_vol_low:.2f}")

    # Сравнение
    if avg_vol_low > 0:
        ratio = avg_vol_high / avg_vol_low
        print(f"\nОТВЕТ: Средний объем торгов в дни роста выше, чем в дни падения в {ratio:.2f} раз.")
    else:
        print("Недостаточно данных для сравнения.")