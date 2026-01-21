import string
import matplotlib.pyplot as plt


def generate_caesar_key(birth_date):
    """Генерація ключа для шифру Цезаря на основі дати народження"""
    # Сума цифр дати (наприклад, 12.05.2004 -> 1+2+0+5+2+0+0+4 = 14)
    date_str = birth_date.replace('.', '')
    key = sum(int(digit) for digit in date_str if digit.isdigit())
    return key % 33  # Для українського алфавіту


def generate_vigenere_key(surname):
    """Генерація ключа для шифру Віженера на основі прізвища"""
    return surname.upper()


def prepare_ukrainian_text(text):
    """Підготовка тексту: приводимо до верхнього регістра, залишаємо лише українські літери"""
    ukrainian_upper = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    text = text.upper()
    # Видаляємо всі символи, крім українських літер та пробілів
    cleaned_text = ''
    for char in text:
        if char in ukrainian_upper or char == ' ':
            cleaned_text += char
    return cleaned_text


def caesar_cipher(text, key, mode='encrypt'):
    """Шифр Цезаря"""
    ukrainian_upper = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    result = ''

    for char in text:
        if char == ' ':
            result += ' '
            continue

        idx = ukrainian_upper.find(char)
        if idx == -1:
            continue

        if mode == 'encrypt':
            new_idx = (idx + key) % 33
        else:  # decrypt
            new_idx = (idx - key) % 33

        result += ukrainian_upper[new_idx]

    return result


def vigenere_cipher(text, key, mode='encrypt'):
    """Шифр Віженера"""
    ukrainian_upper = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    result = ''
    key = key.upper()
    key_len = len(key)
    key_idx = 0

    for char in text:
        if char == ' ':
            result += ' '
            continue

        if key[key_idx % key_len] not in ukrainian_upper:
            continue

        key_char_idx = ukrainian_upper.find(key[key_idx % key_len])
        text_char_idx = ukrainian_upper.find(char)

        if mode == 'encrypt':
            new_idx = (text_char_idx + key_char_idx) % 33
        else:  # decrypt
            new_idx = (text_char_idx - key_char_idx) % 33

        result += ukrainian_upper[new_idx]
        key_idx += 1

    return result


def brute_force_caesar(ciphertext):
    """Метод brute force для шифру Цезаря"""
    ukrainian_upper = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    results = []

    for key in range(33):
        decrypted = ''
        for char in ciphertext:
            if char == ' ':
                decrypted += ' '
                continue

            idx = ukrainian_upper.find(char)
            if idx == -1:
                continue

            new_idx = (idx - key) % 33
            decrypted += ukrainian_upper[new_idx]

        results.append((key, decrypted))

    return results


def frequency_analysis(text):
    """Частотний аналіз тексту"""
    ukrainian_upper = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    freq = {}
    total_letters = 0

    # Підрахунок кількості кожної літери
    for char in text:
        if char in ukrainian_upper:
            freq[char] = freq.get(char, 0) + 1
            total_letters += 1

    # Обчислення відсотків
    percentages = {}
    for letter, count in freq.items():
        percentages[letter] = (count / total_letters * 100) if total_letters > 0 else 0

    return percentages


def compare_algorithms(original, caesar_enc, vigenere_enc):
    """Порівняльний аналіз алгоритмів"""
    print("\n" + "=" * 60)
    print("ПОРІВНЯЛЬНИЙ АНАЛІЗ АЛГОРИТМІВ")
    print("=" * 60)

    comparison = {
        "Критерій": ["Довжина результату", "Читабельність", "Складність ключа", "Унікальність шифру"],
        "Цезарь": [
            len(caesar_enc),
            "Низька (легко розгадати)",
            "Простий (одне число)",
            "Низька (тільки 33 варіанти)"
        ],
        "Віженер": [
            len(vigenere_enc),
            "Вища (складніший для розгадування)",
            "Складний (слово або фраза)",
            "Висока (багато комбінацій)"
        ]
    }

    # Виводимо таблицю порівняння
    print(f"{'Критерій':<25} {'Цезарь':<25} {'Віженер':<25}")
    print("-" * 75)

    for i in range(len(comparison["Критерій"])):
        print(f"{comparison['Критерій'][i]:<25} {comparison['Цезарь'][i]:<25} {comparison['Віженер'][i]:<25}")

    print("\n" + "=" * 60)
    print("ВИСНОВКИ:")
    print("=" * 60)
    print("1. Шифр Цезаря простий, але має низьку стійкість через малу кількість ключів")
    print("2. Шифр Віженера значно стійкіший через використання текстового ключа")
    print("3. Обидва шифри є класичними і не використовуються для сучасного захисту даних")
    print("4. Для підвищення стійкості важливо використовувати довгі та складні ключі")


def visualize_frequencies(original, caesar_enc, vigenere_enc):
    """Візуалізація частотного аналізу"""
    # Аналіз частот для кожного тексту
    orig_freq = frequency_analysis(original)
    caesar_freq = frequency_analysis(caesar_enc)
    vigenere_freq = frequency_analysis(vigenere_enc)

    # Підготовка даних для графіка
    letters = sorted(set(list(orig_freq.keys()) + list(caesar_freq.keys()) + list(vigenere_freq.keys())))

    orig_values = [orig_freq.get(letter, 0) for letter in letters]
    caesar_values = [caesar_freq.get(letter, 0) for letter in letters]
    vigenere_values = [vigenere_freq.get(letter, 0) for letter in letters]

    # Створення графіка
    plt.figure(figsize=(15, 6))

    x = range(len(letters))
    width = 0.25

    plt.bar([i - width for i in x], orig_values, width, label='Оригінальний текст', alpha=0.7)
    plt.bar(x, caesar_values, width, label='Цезарь (зашифрований)', alpha=0.7)
    plt.bar([i + width for i in x], vigenere_values, width, label='Віженер (зашифрований)', alpha=0.7)

    plt.xlabel('Літери')
    plt.ylabel('Частота, %')
    plt.title('Частотний аналіз текстів')
    plt.xticks(x, letters)
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def main():
    """Основна функція програми"""
    print("=" * 60)
    print("ПОРІВНЯЛЬНИЙ АНАЛІЗ КЛАСИЧНИХ АЛГОРИТМІВ ШИФРУВАННЯ")
    print("=" * 60)

    # Персональні дані для генерації ключів
    birth_date = input("Введіть вашу дату народження (дд.мм.рррр): ") or "12.05.2004"
    surname = input("Введіть ваше прізвище: ") or "ПЕТРЕНКО"

    # Тестовий текст
    original_text = "ЗАХИСТ ІНФОРМАЦІЇ ВАЖЛИВА ДИСЦИПЛІНА"
    print(f"\nОригінальний текст: {original_text}")

    # Підготовка тексту
    prepared_text = prepare_ukrainian_text(original_text)

    # Генерація ключів
    caesar_key = generate_caesar_key(birth_date)
    vigenere_key = generate_vigenere_key(surname)

    print(f"\nКлючі для шифрування:")
    print(f"Ключ для Цезаря (сума цифр дати {birth_date}): {caesar_key}")
    print(f"Ключ для Віженера (прізвище): {vigenere_key}")

    # Шифрування
    print("\n" + "-" * 60)
    print("ШИФРУВАННЯ:")
    print("-" * 60)

    caesar_encrypted = caesar_cipher(prepared_text, caesar_key, 'encrypt')
    vigenere_encrypted = vigenere_cipher(prepared_text, vigenere_key, 'encrypt')

    print(f"Текст, зашифрований Цезарем:   {caesar_encrypted}")
    print(f"Текст, зашифрований Віженером: {vigenere_encrypted}")

    # Розшифрування
    print("\n" + "-" * 60)
    print("РОЗШИФРУВАННЯ:")
    print("-" * 60)

    caesar_decrypted = caesar_cipher(caesar_encrypted, caesar_key, 'decrypt')
    vigenere_decrypted = vigenere_cipher(vigenere_encrypted, vigenere_key, 'decrypt')

    print(f"Розшифрований Цезарь:   {caesar_decrypted}")
    print(f"Розшифрований Віженер: {vigenere_decrypted}")

    # Перевірка коректності
    print("\n" + "-" * 60)
    print("ПЕРЕВІРКА КОРЕКТНОСТІ:")
    print("-" * 60)
    print(f"Цезарь:   {'ПРАВИЛЬНО' if caesar_decrypted == prepared_text else 'ПОМИЛКА'}")
    print(f"Віженер: {'ПРАВИЛЬНО' if vigenere_decrypted == prepared_text else 'ПОМИЛКА'}")

    # Криптоаналіз
    print("\n" + "-" * 60)
    print("КРИПТОАНАЛІЗ (BRUTE FORCE ДЛЯ ЦЕЗАРЯ):")
    print("-" * 60)

    brute_results = brute_force_caesar(caesar_encrypted)
    print(f"Знайдено {len(brute_results)} можливих варіантів розшифрування")
    print("\nПерші 5 варіантів:")
    for i in range(min(5, len(brute_results))):
        key, text = brute_results[i]
        print(f"Ключ {key}: {text}")

    # Порівняльний аналіз
    compare_algorithms(prepared_text, caesar_encrypted, vigenere_encrypted)

    # Частотний аналіз
    print("\n" + "-" * 60)
    print("ЧАСТОТНИЙ АНАЛІЗ:")
    print("-" * 60)

    orig_freq = frequency_analysis(prepared_text)
    caesar_freq = frequency_analysis(caesar_encrypted)
    vigenere_freq = frequency_analysis(vigenere_encrypted)

    print("\nНайчастіші літери в оригінальному тексті:")
    for letter, freq in sorted(orig_freq.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{letter}: {freq:.2f}%")

    print("\nНайчастіші літери в тексті Цезаря:")
    for letter, freq in sorted(caesar_freq.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{letter}: {freq:.2f}%")

    print("\nНайчастіші літери в тексті Віженера:")
    for letter, freq in sorted(vigenere_freq.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{letter}: {freq:.2f}%")

    # Візуалізація
    print("\n" + "-" * 60)
    print("ГЕНЕРУЄМО ГРАФІК ЧАСТОТНОГО АНАЛІЗУ...")
    print("-" * 60)
    visualize_frequencies(prepared_text, caesar_encrypted, vigenere_encrypted)

    print("\n" + "=" * 60)
    print("РОБОТУ ПРОГРАМИ ЗАВЕРШЕНО!")
    print("=" * 60)


if __name__ == "__main__":
    main()
