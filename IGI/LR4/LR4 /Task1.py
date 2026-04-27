import csv
import pickle

import Input


class InfoMixin:
    """Миксин для предоставления информации о названии класса объекта."""

    def get_class_info(self):
        """Возвращает строку с именем текущего класса."""
        return f"Class: {self.__class__.__name__}"


class Person(InfoMixin):
    """
    Базовый класс, представляющий человека.

    Attributes:
        person_count (int): Статический счетчик созданных экземпляров класса Person.
    """
    person_count = 0

    def __init__(self, name):
        """
        Инициализирует объект Person.

        Args:
            name (str): Имя человека.
        """
        self._name = name
        Person.person_count += 1

    @property
    def name(self):
        """Property для получения имени человека."""
        return self._name

    @name.setter
    def name(self, value):
        """
        Устанавливает имя человека с проверкой на пустую строку.

        Raises:
            ValueError: Если имя пустое или не является строкой.
        """
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string.")
        self._name = value

    def __str__(self):
        """Возвращает строковое представление объекта Person."""
        return f"Person: {self.name}"


class Student(Person):
    """
    Класс, представляющий студента и его спортивные результаты. Наследуется от Person.
    """

    def __init__(self, name, run_100m, long_jump):
        """
        Инициализирует объект Student.

        Args:
            name (str): Имя студента.
            run_100m (float/str): Время бега на 100м в секундах.
            long_jump (float/str): Дистанция прыжка в длину в метрах.
        """
        super().__init__(name)
        self._run_100m = float(run_100m)
        self._long_jump = float(long_jump)

    @property
    def run_100m(self):
        """Возвращает результат бега на 100м."""
        return self._run_100m

    @property
    def long_jump(self):
        """Возвращает результат прыжка в длину."""
        return self._long_jump

    def __str__(self):
        """Возвращает форматированную строку с результатами студента."""
        return f"Student {self.name} | 100m: {self.run_100m}s | Jump: {self.long_jump}m"

    def __lt__(self, other):
        """
        Определяет логику сравнения студентов ('меньше чем') для сортировки.
        Сравнение идет по интегральному баллу (бег + прыжок).
        """
        if not isinstance(other, Student):
            raise TypeError("Can only compare with Student instances.")
        self_score = -self.run_100m + self.long_jump * 10
        other_score = -other.run_100m + other.long_jump * 10
        return self_score < other_score


class CsvSerializer:
    """Класс для сохранения и загрузки данных в формате CSV."""
    def save(self, data, filename):
        """
        Сохраняет словарь данных в CSV файл с использованием DictWriter.

        Args:
            data (dict): Словарь с результатами студентов.
            filename (str): Путь к файлу.
        """
        try:
            #Определяем заголовки (они же будут ключами для DictWriter)
            fieldnames = ["Name", "100m", "LongJump"]
            with open(filename, mode='w', newline='', encoding='utf-8') as f:
                #Создаем объект DictWriter, передавая заголовки
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                #Записываем строку заголовков (автоматически из fieldnames)
                writer.writeheader()
                #Перебираем данные
                for name, results in data.items():
                    writer.writerow({
                        "Name": name,
                        "100m": results["100m"],
                        "LongJump": results["long_jump"]  # Маппинг ключа
                    })
        except IOError as e:
            print(f"Error saving CSV: {e}")

    def load(self, filename):
        """
        Загружает данные из CSV файла и возвращает словарь.

        Returns:
            dict: Словарь с данными студентов.
        """
        data = {}
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data[row["Name"]] = {
                        "100m": float(row["100m"]),
                        "long_jump": float(row["LongJump"])
                    }
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except ValueError as e:
            print(f"Data type conversion error: {e}")
        return data


class PickleSerializer:
    """Класс для сериализации данных с помощью модуля pickle (бинарный формат)."""

    def save(self, data, filename):
        """Сохраняет объект данных в файл pickle."""
        try:
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
        except IOError as e:
            print(f"Error saving Pickle: {e}")

    def load(self, filename):
        """Загружает данные из файла pickle."""
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return {}
        except pickle.PickleError as e:
            print(f"Pickle error: {e}")
            return {}


class GtoManager:
    """
    Класс для управления списком студентов и анализа их соответствия нормам ГТО.
    """

    def __init__(self, norm_100m, norm_long_jump):
        """
        Инициализирует менеджер с заданными нормативами.

        Args:
            norm_100m (float): Максимально допустимое время бега.
            norm_long_jump (float): Минимально допустимая длина прыжка.
        """
        self.norm_100m = norm_100m
        self.norm_long_jump = norm_long_jump
        self.students = []

    def load_data(self, data_dict):
        """Преобразует словарь с данными в список объектов Student."""
        self.students = []
        for name, stats in data_dict.items():
            self.students.append(Student(name, stats["100m"], stats["long_jump"]))

    def get_failed_students(self):
        """Возвращает список студентов, не выполнивших хотя бы один норматив."""
        failed = []
        for s in self.students:
            if s.run_100m > self.norm_100m or s.long_jump < self.norm_long_jump:
                failed.append(s)
        return failed

    def get_passed_count(self):
        """Возвращает количество студентов, успешно сдавших все нормы."""
        passed_count = len(self.students) - len(self.get_failed_students())
        return passed_count

    def get_top_3(self):
        """Возвращает список из 3-х лучших студентов по результатам."""
        sorted_students = sorted(self.students, reverse=True)
        return sorted_students[:3]

    def search_student(self, name):
        """
        Ищет студента в списке по имени (без учета регистра).

        Returns:
            Student/None: Объект студента, если найден, иначе None.
        """
        for s in self.students:
            if s.name.lower() == name.lower():
                return s
        return None


def initial_data():
    """Возвращает начальный набор данных для тестирования программы."""
    return {
        "Danilchuk": {"100m": 13.2, "long_jump": 2.1},
        "Petrov Petr": {"100m": 14.5, "long_jump": 1.8},
        "Smirnov Smirec": {"100m": 12.8, "long_jump": 2.3},
        "Sidorov Sidr": {"100m": 15.0, "long_jump": 1.7},
        "Kuznetsov Kuznec": {"100m": 13.0, "long_jump": 2.2},
    }


def task1():
    """Основная функция программы: управление интерфейсом и логикой обработки данных."""
    print("=== GTO Norms Analysis Program ===")

    data = initial_data()
    csv_file = "gto_data.csv"
    pkl_file = "gto_data.pkl"

    serializers = [CsvSerializer(), PickleSerializer()]
    files = [csv_file, pkl_file]

    serializers[0].save(data, files[0])
    serializers[1].save(data, files[1])

    manager = GtoManager(norm_100m=13.5, norm_long_jump=2.0)

    while True:
        print("\n--- Main Menu ---")
        print("1. Load data from CSV")
        print("2. Load data from Pickle")
        print("3. Set GTO norms")
        print("4. Show failed students")
        print("5. Show passed students count")
        print("6. Show top 3 students")
        print("7. Search for a student")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == '0':
            print("Exiting program. Goodbye!")
            break

        elif choice == '1':
            loaded = serializers[0].load(csv_file)
            manager.load_data(loaded)
            print("Data loaded from CSV successfully!")

        elif choice == '2':
            loaded = serializers[1].load(pkl_file)
            manager.load_data(loaded)
            print("Data loaded from Pickle successfully!")

        elif choice == '3':
            manager.norm_100m = Input.get_valid_float("Enter max time for 100m (seconds): ")
            manager.norm_long_jump = Input.get_valid_float("Enter min distance for long jump (meters): ")
            print("Norms updated successfully.")

        elif choice == '4':
            if not manager.students:
                print("Please load data first!")
                continue
            failed = manager.get_failed_students()
            print("\n--- Students who failed ---")
            for s in failed:
                print(s)

        elif choice == '5':
            if not manager.students:
                print("Please load data first!")
                continue
            count = manager.get_passed_count()
            print(f"\nTotal students who passed the norms: {count}")

        elif choice == '6':
            if not manager.students:
                print("Please load data first!")
                continue
            top3 = manager.get_top_3()
            print("\n--- Top 3 Students ---")
            for i, s in enumerate(top3, 1):
                print(f"{i}. {s}")

        elif choice == '7':
            if not manager.students:
                print("Please load data first!")
                continue
            name_to_search = input("Enter student name: ").strip()
            student = manager.search_student(name_to_search)
            if student:
                print(f"\nFound: {student}")
                print(student.get_class_info())
            else:
                print("\nStudent not found.")

        else:
            print("Invalid option. Please try again.")