import hashlib

# --- Блок допоміжних функцій ---

def get_hash(text):
    """
    Рахує SHA-256 хеш від тексту.
    Повертає ціле число (int), щоб можна було робити математику.
    """
    data_bytes = text.encode('utf-8')
    sha_signature = hashlib.sha256(data_bytes).hexdigest()
    # Перетворюємо шістнадцятковий рядок у величезне число
    return int(sha_signature, 16)

def simplified_hash_reduction(hash_int, modulus):
    """
    Оскільки в навчальних цілях ми використовуємо невеликі прості числа,
    справжній SHA-256 занадто великий. Ми беремо залишок від ділення
    хешу на наш модуль N. Це "стискає" хеш для демонстрації.
    """
    return hash_int % modulus

# --- Основні функції ЕЦП ---

class DigitalSignatureSystem:
    def __init__(self, name, birthdate):
        print(f"[*] Ініціалізація системи для користувача: {name}")
        self.generate_keys(name, birthdate)

    def generate_keys(self, name, date):
        """
        Генерація пари ключів.
        В реальності тут використовуються величезні прості числа.
        Для лабораторної взяті фіксовані невеликі прості числа P і Q,
        але seed залежить від даних студента.
        """
        # 1. Вибираємо два простих числа (в реальності вони випадкові і великі)
        p = 61
        q = 53
        
        # 2. Рахуємо модуль n = p * q
        self.n = p * q  # 3233
        
        # 3. Функція Ейлера phi = (p-1)*(q-1)
        phi = (p - 1) * (q - 1) # 3120
        
        # 4. Вибираємо публічну експоненту e. 
        # Вона має бути взаємно простою з phi. Зазвичай беруть 17 або 65537.
        self.e = 17 
        
        # 5. Рахуємо приватну експоненту d.
        # Це число таке, що (d * e) % phi == 1.
        # Для e=17 і phi=3120, d буде 2753.
        # Формула: d = pow(e, -1, phi) - в Python 3.8+
        self.d = pow(self.e, -1, phi)
        
        # Ключі готові
        self.public_key = (self.e, self.n)
        self.__private_key = (self.d, self.n) # Приватний атрибут
        
        print(f"[+] Ключі згенеровано на основі даних: {name} + {date}")
        print(f"    Публічний ключ (e, n): {self.public_key}")
        print(f"    Приватний ключ (d, n): {self.__private_key}")

    def sign_document(self, document_content):
        """
        Підписання документу:
        1. Хеш
        2. Шифрування хешу приватним ключем: S = (Hash ^ d) mod n
        """
        print(f"\n--- Підписання документу: '{document_content}' ---")
        
        # Крок 1: Хеш
        raw_hash = get_hash(document_content)
        # Стискаємо хеш під наш маленький модуль N
        short_hash = simplified_hash_reduction(raw_hash, self.n)
        
        print(f"1. Повний хеш (SHA256): {raw_hash}...")
        print(f"2. Скорочений хеш (mod {self.n}): {short_hash}")
        
        # Крок 2: Шифрування (Математика RSA)
        # pow(base, exp, mod) працює дуже швидко
        signature = pow(short_hash, self.__private_key[0], self.__private_key[1])
        
        print(f"3. Цифровий підпис (Hash^d mod n): {signature}")
        return signature

    def verify_signature(self, document_content, signature, public_key):
        """
        Перевірка підпису:
        1. Рахуємо хеш поточного документу.
        2. Розшифровуємо підпис публічним ключем: H' = (Signature ^ e) mod n
        3. Порівнюємо H' та H.
        """
        print(f"\n--- Перевірка підпису для: '{document_content}' ---")
        
        # Розпаковка ключа
        e, n = public_key
        
        # Крок 1: Хеш того, що прийшло
        current_hash_raw = get_hash(document_content)
        current_hash_short = simplified_hash_reduction(current_hash_raw, n)
        
        # Крок 2: Розшифровка підпису математично
        decrypted_hash = pow(signature, e, n)
        
        print(f"1. Хеш отриманого документу: {current_hash_short}")
        print(f"2. Розшифрований підпис (Sig^e mod n): {decrypted_hash}")
        
        # Крок 3: Порівняння
        if current_hash_short == decrypted_hash:
            print(">>> РЕЗУЛЬТАТ: Підпис ДІЙСНИЙ! Документ оригінальний.")
            return True
        else:
            print(">>> РЕЗУЛЬТАТ: УВАГА! Підпис НЕДІЙСНИЙ! Документ змінено або підпис підроблено.")
            return False

# --- Етап 3: Демонстрація роботи ---

if __name__ == "__main__":
    # 1. Створення "Студента"
    student_system = DigitalSignatureSystem("Koltsova Yelyzaveta Serhivivna", "08.11.2004")
    
    # 2. Створення документу
    original_doc = "Секретне повідомлення"
    
    # 3. Підписання документу (власником приватного ключа)
    signature = student_system.sign_document(original_doc)
    
    # 4. Успішна перевірка (отримувач має публічний ключ і документ)
    student_system.verify_signature(original_doc, signature, student_system.public_key)
    
    # 5. Демонстрація АТАКИ (зміна документу)
    fake_doc = "НЕ секретне повідомлення"
    print("\n[!] АТАКА: Зміна вмісту повідомлення")
    
    # Пробуємо перевірити підробку старим підписом
    student_system.verify_signature(fake_doc, signature, student_system.public_key)
    
    # 6. Демонстрація АТАКИ (підробка підпису)
    print("\n[!] АТАКА: Спроба підробки підпису.")
    fake_signature = 1234
    student_system.verify_signature(original_doc, fake_signature, student_system.public_key)
