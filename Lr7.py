import os
import time
import hashlib
import base64
from cryptography.fernet import Fernet
from PIL import Image

# --- МОДУЛЬ АНАЛІТИКИ ---
class SecurityAnalytics:
    def __init__(self):
        self.stats = []
        self.start_timer = 0

    def start_stage(self, stage_name):
        self.start_timer = time.time()
        print(f"\n[INFO] Початок етапу: {stage_name}...")

    def end_stage(self, stage_name, data_size_bytes=0):
        elapsed = time.time() - self.start_timer
        self.stats.append({
            "stage": stage_name,
            "time": elapsed,
            "size": data_size_bytes
        })
        print(f"[OK] Етап завершено. Час: {elapsed:.4f} сек. Розмір даних: {data_size_bytes} байт.")

    def print_report(self):
        print("\n" + "="*40)
        print(" АНАЛІТИЧНИЙ ЗВІТ ЕФЕКТИВНОСТІ")
        print("="*40)
        print(f"{'Етап':<25} | {'Час (сек)':<10} | {'Розмір (байт)':<10}")
        print("-" * 50)
        for item in self.stats:
            print(f"{item['stage']:<25} | {item['time']:<10.4f} | {item['size']:<10}")
        print("-" * 50)

# --- МОДУЛЬ ШИФРУВАННЯ (AES) ---
class CryptoModule:
    def __init__(self, password):
        # Генеруємо ключ із пароля (SHA-256 -> base64)
        key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
        self.cipher = Fernet(key)

    def encrypt(self, text):
        return self.cipher.encrypt(text.encode())

    def decrypt(self, encrypted_bytes):
        return self.cipher.decrypt(encrypted_bytes).decode()

# --- МОДУЛЬ СТЕГАНОГРАФІЇ (LSB) ---
class StegoModule:
    def __init__(self, delimiter="#####"):
        self.delimiter = delimiter

    def _to_bin(self, data_bytes):
        # Перетворюємо байти в рядок бітів
        binary_str = ""
        # data_bytes може бути як bytes так і str, приводимо до спільного знаменника
        if isinstance(data_bytes, str):
            data_bytes = data_bytes.encode()
        
        for byte in data_bytes:
            binary_str += format(byte, '08b')
        return binary_str

    def hide(self, image_path, output_path, data_bytes):
        img = Image.open(image_path).convert('RGB')
        # Додаємо делімітер до даних, щоб знати де кінець
        full_data = data_bytes + self.delimiter.encode()
        binary_data = self._to_bin(full_data)
        
        data_len = len(binary_data)
        pixels = img.load()
        width, height = img.size
        
        idx = 0
        for y in range(height):
            for x in range(width):
                if idx >= data_len: break
                r, g, b = pixels[x, y]
                
                # Записуємо біти у канали R, G, B
                if idx < data_len:
                    r = (r & ~1) | int(binary_data[idx])
                    idx += 1
                if idx < data_len:
                    g = (g & ~1) | int(binary_data[idx])
                    idx += 1
                if idx < data_len:
                    b = (b & ~1) | int(binary_data[idx])
                    idx += 1
                
                pixels[x, y] = (r, g, b)
            if idx >= data_len: break
            
        img.save(output_path, "PNG")
        return os.path.getsize(output_path)

    def extract(self, image_path):
        img = Image.open(image_path).convert('RGB')
        pixels = img.load()
        width, height = img.size
        
        binary_data = ""
        # Читаємо біти
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)

        # Конвертуємо біти в байти
        all_bytes = bytearray()
        for i in range(0, len(binary_data), 8):
            byte_chunk = binary_data[i:i+8]
            if len(byte_chunk) < 8: break
            all_bytes.append(int(byte_chunk, 2))

        # Шукаємо делімітер
        try:
            # Перетворюємо в bytes для пошуку
            extracted_raw = bytes(all_bytes)
            delimiter_bytes = self.delimiter.encode()
            
            end_index = extracted_raw.find(delimiter_bytes)
            if end_index != -1:
                return extracted_raw[:end_index]
            else:
                return b"" # Не знайдено
        except Exception:
            return b""

# --- ГОЛОВНА ЛОГІКА (Main) ---
if __name__ == "__main__":
    # 0. Підготовка
    analytics = SecurityAnalytics()
    password = "KoltsovaYelyzavetaSerhivivna08.11.2004"
    secret_text = "Секретне повідомлення"
    
    # Створюємо пусте зображення-контейнер, якщо немає
    base_image = "container.png"
    stego_image = "protected_container.png"
    if not os.path.exists(base_image):
        Image.new('RGB', (200, 200), color='blue').save(base_image)

    print(f"Вхідний текст: '{secret_text}'")
    print(f"Пароль шифрування: '{password}'")

    # --- ЕТАП 1: Шифрування (AES) ---
    analytics.start_stage("1. AES Шифрування")
    crypto = CryptoModule(password)
    encrypted_data = crypto.encrypt(secret_text)
    # Записуємо розмір зашифрованих даних
    analytics.end_stage("1. AES Шифрування", len(encrypted_data))
    
    print(f"   -> Зашифровані байти: {encrypted_data[:20]}...")

    # --- ЕТАП 2: Приховування (LSB) ---
    analytics.start_stage("2. LSB Приховування")
    stego = StegoModule()
    stego_size = stego.hide(base_image, stego_image, encrypted_data)
    analytics.end_stage("2. LSB Приховування", stego_size)

    print(f"   -> Дані сховано в '{stego_image}'")

    # --- ЕТАП 3: Перевірка відновлення ---
    print("\n--- Імітація передачі файлу та відновлення ---")
    
    analytics.start_stage("3. Вилучення з фото")
    extracted_bytes = stego.extract(stego_image)
    analytics.end_stage("3. Вилучення з фото", len(extracted_bytes))
    
    if not extracted_bytes:
        print("[!] Помилка: Не вдалося витягнути дані з картинки.")
        exit()

    analytics.start_stage("4. AES Дешифрування")
    try:
        decrypted_text = crypto.decrypt(extracted_bytes)
        analytics.end_stage("4. AES Дешифрування", len(decrypted_text))
        print(f"\n[SUCCESS] Відновлений текст: '{decrypted_text}'")
    except Exception as e:
        print(f"\n[FAIL] Помилка дешифрування: {e}")

    # --- ЗВІТ ---
    analytics.print_report()
