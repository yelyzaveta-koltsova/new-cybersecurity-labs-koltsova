import sqlite3

# --- 1. Налаштування бази даних ---

def init_db():
    """
    Створює тимчасову базу даних в оперативній пам'яті 
    """
    # Підключаємось до БД 
    conn = sqlite3.connect(":memory:") 
    cursor = conn.cursor()
    
    # Створюємо таблицю users
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT,
            salary INTEGER
        )
    """)
    
    # Наповнюємо тестовими даними
    users_data = [
        (1, 'admin', 'SuperSecretPass', 'administrator', 5000),
        (2, 'ivan_student', '12345', 'user', 0),
        (3, 'petro_teacher', 'math_rules', 'moderator', 1500),
        (4, 'guest', 'guest', 'visitor', 0)
    ]
    
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", users_data)
    conn.commit()
    print("[*] База даних успішно створена та наповнена.")
    return conn

# --- 2. Вразлива реалізація ---

def vulnerable_search(conn, user_input):
    """
    Функція пошуку з ін'єкцією
    """
    cursor = conn.cursor()
    
    print(f"\n--- [ВРАЗЛИВИЙ ПОШУК] Запит: '{user_input}' ---")
    
  
    # Ми просто вставляємо текст користувача всередину запиту.
    sql_query = f"SELECT * FROM users WHERE username = '{user_input}'"
    
    # Виводимо, як виглядає фінальний SQL запит для наочності
    print(f"[DEBUG] Виконується SQL: {sql_query}")
    
    try:
        # cursor.executescript() дозволяє виконувати кілька команд, 
        # але для демонстрації SELECT достатньо звичайного execute
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        if results:
            print(f"[+] Знайдено записів: {len(results)}")
            for row in results:
                print(f"    -> ID: {row[0]}, Login: {row[1]}, Pass: {row[2]}, Salary: ${row[4]}")
        else:
            print("[-] Нічого не знайдено.")
            
    except sqlite3.Error as e:
        print(f"[!] Помилка SQL: {e}")

# --- 3. Захищена реалізація ---

def secure_search(conn, user_input):
    """
    Функція пошуку із захистом.
    Використовує параметризовані запити
    """
    cursor = conn.cursor()
    
    print(f"\n--- [ЗАХИЩЕНИЙ ПОШУК] Запит: '{user_input}' ---")
    
    sql_query = "SELECT * FROM users WHERE username = ?"
    
    print(f"[DEBUG] Шаблон SQL: {sql_query}")
    print(f"[DEBUG] Параметри: ('{user_input}',)")
    
    # Передаємо параметри окремим аргументом 
    # Драйвер БД екранує спецсимволи
    cursor.execute(sql_query, (user_input,))
    results = cursor.fetchall()
    
    if results:
        print(f"[+] Знайдено записів: {len(results)}")
        for row in results:
            print(f"    -> {row}")
    else:
        print("[-] Нічого не знайдено (ін'єкція не спрацювала).")

# --- 4. Демонстрація (Main) ---

if __name__ == "__main__":
    # Ініціалізація
    db_conn = init_db()
    
    # Сценарій 1: Чесний пошук
    # Користувач просто шукає 'admin'
    vulnerable_search(db_conn, "admin")
    
    # Сценарій 2: SQL Injection (Атака)
    # Зловмисник вводить спеціальний рядок, щоб умова стала завжди істинною (OR 1=1)
    # Символ -- (або #) коментує решту запиту, але в SQLite простіше без нього, якщо це кінець рядка.
    payload = "admin' OR '1'='1"
    
    print("\n" + "="*50)
    print("АТАКА")
    print("="*50)
    
    # Запускаємо атаку на вразливу функцію
    vulnerable_search(db_conn, payload)
    
    print("\n" + "="*50)
    print("ПЕРЕВІРКА ЗАХИСТУ")
    print("="*50)
    
    # Запускаємо ту ж саму атаку на захищену функцію
    secure_search(db_conn, payload)
    
    db_conn.close()
