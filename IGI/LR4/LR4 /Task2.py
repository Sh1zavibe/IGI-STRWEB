import re
import zipfile


def task2():
    """
    Выполняет комплексный анализ текстового файла и архивирует результаты.

    Функция считывает данные из 'input.txt', проводит статистический анализ текста
    с использованием регулярных выражений, сохраняет отчет в 'result.txt'
    и упаковывает его в ZIP-архив.

    Основные этапы анализа:
    1. Подсчет типов предложений (повествовательные, вопросительные, восклицательные).
    2. Поиск смайликов (например, ;-) или :-( ).
    3. Вычисление средней длины слова и предложения.
    4. Поиск смешанных слов (буквы + цифры) и IP-адресов.
    5. Фильтрация слов по длине и поиск самого короткого слова, заканчивающегося на 'w'.
    6. Сортировка всех слов текста по возрастанию длины.

    Файловые операции:
    - Чтение: input.txt
    - Запись: result.txt
    - Архив: result.zip
    """
    input_filename = "input.txt"
    output_filename = "result.txt"
    archive_filename = "result.zip"

    # Чтение исходного текста
    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_filename} не найден.")
        return

    # Анализ предложений
    # [^!?]*\.  - ищем точку, перед которой нет ! или ?
    decl_sentences = len(re.findall(r'[^!?]*\.(?!\.)', text))
    inter_sentences = len(re.findall(r'[^!.?]*\?', text))
    excl_sentences = len(re.findall(r'[^!.?]*!', text))
    total_sentences = decl_sentences + inter_sentences + excl_sentences

    # Поиск смайликов
    smile_pattern = r'[;:][-]*([()\[\]])\1*'
    smilies = re.findall(smile_pattern, text)
    count_smilies = len(smilies)

    # Статистика слов
    words = re.findall(r'\b\w+\b', text)
    total_words_len = sum(len(w) for w in words)
    avg_word_len = total_words_len / len(words) if words else 0
    avg_sentence_len = total_words_len / total_sentences if total_sentences > 0 else 0

    words_mixed = re.findall(r'\b(?:[a-z]+\d[a-z\d]*|\d+[a-z][a-z\d]*)\b', text, flags=re.IGNORECASE)

    # Поиск IPv4 адресов
    ip_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    found_ips = re.findall(ip_pattern, text)

    # Списки слов
    words_less_6 = [w for w in words if len(w) < 6]
    words_ending_w = re.findall(r'\b[wW]\w*\b', text)
    shortest_w = min(words_ending_w, key=len) if words_ending_w else "Не найдено"

    # Сортировка слов
    sorted_words = sorted(words, key=len)

    # Формирование отчета
    results = [
        "--- ОБЩАЯ ИНФОРМАЦИЯ ---",
        f"Всего предложений: {total_sentences}",
        f"  - Повествовательных: {decl_sentences}",
        f"  - Вопросительных: {inter_sentences}",
        f"  - Побудительных: {excl_sentences}",
        f"Средняя длина предложения (в символах слов): {avg_sentence_len:.2f}",
        f"Средняя длина слова: {avg_word_len:.2f} симв.",
        f"Количество смайликов: {count_smilies}",
        "\n--- ЗАДАНИЯ ПО ВАРИАНТУ ---",
        f"Слова (буквы+цифры): {', '.join(words_mixed)}",
        f"Найденные IP-адреса: {', '.join(found_ips)}",
        f"Кол-во слов < 6 символов: {len(words_less_6)}",
        f"Самое короткое слово на 'w': {shortest_w}",
        f"Слова по возрастанию длины: {' '.join(sorted_words)}"
    ]

    result_text = "\n".join(results)

    # Запись в файл
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(result_text)

    # Архивирование
    with zipfile.ZipFile(archive_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(output_filename)

    print(f"Анализ завершен. Результаты в {output_filename} и {archive_filename}")