from PIL import Image
import os

# --- Допоміжні функції ---

def text_to_binary(text):
    """
    Перетворює текст у рядок бітів.
    Кожен символ кодується 8 бітами (ASCII/UTF-8 byte).
    """
    binary_string = ''
    # Перетворюємо текст в байти, а потім кожен байт у бінарний вигляд
    # format(byte, '08b') робить з числа рядок типу '01100001'
    encoded_text = text.encode('utf-8')
    for byte in encoded_text:
        binary_string += format(byte, '08b')
    return binary_string

def binary_to_text(binary_string):
    """
    Перетворює рядок бітів назад у текст.
    """
    bytes_data = bytearray()
    # Беремо по 8 біт і робимо з них число -> символ
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        # Конвертуємо тільки повні байти
        if len(byte) == 8:
            bytes_data.append(int(byte, 2))
    
    try:
        return bytes_data.decode('utf-8')
    except UnicodeDecodeError:
        return "Помилка декодування (можливо, невірні дані)"

# --- Основні функції (Етап 2) ---

def hide_message(image_path, output_path, secret_text):
    print(f"[*] Починаємо приховування тексту в {image_path}...")
    
    # Відкриваємо зображення
    img = Image.open(image_path)
    # Конвертуємо в RGB, про всяк випадок
    img = img.convert("RGB")
    width, height = img.size
    
    # Додаємо маркер кінця повідомлення, щоб знати, коли стоп
    DELIMITER = "#####"
    full_text = secret_text + DELIMITER
    
    # Отримуємо бінарний код
    binary_msg = text_to_binary(full_text)
    data_len = len(binary_msg)
    
    # Перевірка, чи влізе текст в картинку
    # В кожному пікселі 3 канали (R, G, B), тому можемо сховати 3 біти
    max_capacity = width * height * 3
    if data_len > max_capacity:
        print(f"[!] Помилка: Текст занадто великий для цієї картинки! Потрібно більше пікселів.")
        return

    print(f"[*] Довжина повідомлення (біт): {data_len}")
    print(f"[*] Максимальна ємність картинки (біт): {max_capacity}")

    # Завантажуємо пікселі для редагування
    pixels = img.load()

    data_index = 0
    
    # Проходимо по всіх пікселях (цикли x та y)
    for y in range(height):
        for x in range(width):
            if data_index >= data_len:
                break
            
            # Отримуємо поточний піксель (R, G, B)
            r, g, b = pixels[x, y]
            
            # Змінюємо R (червоний)
            if data_index < data_len:
                # Логіка: обнуляємо останній біт (& ~1) і додаємо біт повідомлення (| int(...))
                r = (r & ~1) | int(binary_msg[data_index])
                data_index += 1
                
            # Змінюємо G (зелений)
            if data_index < data_len:
                g = (g & ~1) | int(binary_msg[data_index])
                data_index += 1
                
            # Змінюємо B (синій)
            if data_index < data_len:
                b = (b & ~1) | int(binary_msg[data_index])
                data_index += 1
            
            # Записуємо змінений піксель назад
            pixels[x, y] = (r, g, b)
        
        if data_index >= data_len:
            break
            
    # Зберігаємо результат
    # ВАЖЛИВО: зберігати в PNG, бо JPG зіпсує пікселі стисненням
    img.save(output_path, "PNG")
    print(f"[+] Успішно збережено в файл: {output_path}")


def extract_message(image_path):
    print(f"[*] Спроба витягнути повідомлення з {image_path}...")
    
    img = Image.open(image_path)
    img = img.convert("RGB")
    width, height = img.size
    pixels = img.load()
    
    binary_data = ""
    DELIMITER = "#####"
    
    # Проходимо по пікселях і збираємо останні біти
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Витягуємо останні біти (операція AND 1)
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
            
    # Перевіряємо кожні 8 біт (1 байт), чи не знайшли ми маркер
    # Але для спрощення просто конвертуємо все в текст і шукаємо маркер
    # (В реальних задачах краще перевіряти "на льоту", щоб не крутити зайві цикли)
    
    # Розбиваємо по 8 біт
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    
    decoded_msg = ""
    for byte in all_bytes:
        # Конвертуємо байт в символ
        decoded_msg += chr(int(byte, 2))
        # Перевіряємо чи є маркер в кінці нашого зібраного рядка
        if decoded_msg.endswith(DELIMITER):
            # Відрізаємо маркер і виходимо
            print("[+] Повідомлення знайдено!")
            return decoded_msg[:-len(DELIMITER)]
            
    return "[!] Повідомлення або маркер не знайдено."

# --- Етап 3: Демонстрація на персональних даних ---

if __name__ == "__main__":
    # Вхідні дані
    original_image = "input_image.png" # Потрібно мати будь-яку картинку поруч зі скриптом
    stego_image = "secret_image.png"
    
    # Персональні дані
    my_data = "Koltsova Yelyzaveta Serhivivna 08.11.2004"
    
    # Створюємо тестову картинку, якщо її немає (щоб код працював одразу)
    if not os.path.exists(original_image):
        print("Створено тестове зображення")
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(original_image)

    # 1. Ховаємо повідомлення
    hide_message(original_image, stego_image, my_data)
    
    print("-" * 30)
    
    # 2. Витягуємо повідомлення
    extracted_text = extract_message(stego_image)
    print(f"Розшифрований текст:\n>> {extracted_text}")
    
    print("-" * 30)
    
    # --- Етап 4: Аналіз ---
    
    size_orig = os.path.getsize(original_image)
    size_stego = os.path.getsize(stego_image)
    
    print("АНАЛІЗ РЕЗУЛЬТАТІВ:")
    print(f"Розмір оригінала: {size_orig} байт")
    print(f"Розмір з секретом: {size_stego} байт")
    print(f"Різниця: {size_stego - size_orig} байт")
    print("Візуально картинки ідентичні, оскільки зміна кольору на 1 одиницю непомітна.")
