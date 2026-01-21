import base64
import hashlib
from cryptography.fernet import Fernet

# --- Клас для роботи з шифруванням ---

class SecureMessenger:
    def __init__(self):
        self.key = None
        self.cipher_suite = None

    def generate_key_from_data(self, personal_data):
        """
        Генерує валідний 32-байтовий ключ для AES на основі будь-якого тексту.
        Використовуємо хешування (SHA-256), щоб перетворити рядок
        будь-якої довжини у фіксований набір байтів.
        """
        print(f"[*] Генерація ключа на основі даних: '{personal_data}'")
        
        # 1. Отримуємо хеш (32 байти)
        digest = hashlib.sha256(personal_data.encode()).digest()
        
        # 2. Fernet вимагає url-safe base64 кодування ключа
        self.key = base64.urlsafe_b64encode(digest)
        
        # 3. Ініціалізуємо шифратор
        self.cipher_suite = Fernet(self.key)
        
        print(f"    -> Згенерований ключ (base64): {self.key.decode()}")

    def encrypt_message(self, message):
        """
        Шифрує повідомлення.
        Повертає зашифровані байти (токен).
        """
        if not self.cipher_suite:
            return "Помилка: Ключ не встановлено!"
        
        # Fernet вимагає байти на вхід, тому message.encode()
        encrypted_text = self.cipher_suite.encrypt(message.encode('utf-8'))
        return encrypted_text

    def decrypt_message(self, encrypted_token):
        """
        Розшифровує повідомлення.
        """
        if not self.cipher_suite:
            return "Помилка: Ключ не встановлено!"
        
        try:
            decrypted_text = self.cipher_suite.decrypt(encrypted_token)
            return decrypted_text.decode('utf-8')
        except Exception as e:
            return f"Помилка розшифрування: Невірний ключ або пошкоджені дані! ({e})"

# --- Етап 3: Демонстрація (Main) ---

if __name__ == "__main__":
    

    # В симетричному шифруванні обидві сторони повинні мати однаковий ключ.
    shared_secret_data = "KoltsovaYelyzavetaSerhivivna08.11.2004"
    
    # 1. Сторона ВІДПРАВНИКА 
    print("\n[1] ВІДПРАВНИК:")
    sender = SecureMessenger()
    sender.generate_key_from_data(shared_secret_data)
    
    email_text = "Секретне повідомлення"
    print(f"    Оригінальний текст: {email_text}")
    
    encrypted_email = sender.encrypt_message(email_text)
    print(f"    Зашифровані дані (те, що йде по мережі):")
    print(f"    >> {encrypted_email}")
    
   
    
    
    # 2. Сторона ОТРИМУВАЧА
    print("[2] ОТРИМУВАЧ:")
    receiver = SecureMessenger()
    
    # Отримувач вводить ту саму секретну фразу, щоб отримати той самий ключ
    # Спробуємо спочатку правильний ключ
    print("    Спроба генерації ключа з правильними даними...")
    receiver.generate_key_from_data(shared_secret_data)
    
    decrypted_text = receiver.decrypt_message(encrypted_email)
    print(f"    Результат розшифрування: {decrypted_text}")
    
    # 3. Демонстрація перехоплення 
    print("\n[3] Спроба зламу:")
    hacker = SecureMessenger()
    # Зловмисник не знає секретної фрази, пробує підібрати
    hacker.generate_key_from_data("Admin123") 
    
    hacker_try = hacker.decrypt_message(encrypted_email)
    print(f"    Результат злому: {hacker_try}")
