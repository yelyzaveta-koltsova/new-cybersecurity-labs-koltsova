import re

def analyze_password(password, name, birth_date):
    """
    Аналізує пароль на основі особистих даних та різних критеріїв.

    Args:
        password (str): Пароль для аналізу.
        name (str): Ім'я користувача.
        birth_date (str): Дата народження користувача (у форматі DD.MM.YYYY).

    Returns:
        tuple: Оцінка безпеки (1-10) та список рекомендацій.
    """

    score = 0
    recommendations = []

    # 1. Аналіз зв'язку з особистими даними
    name_lower = name.lower()
    if name_lower in password.lower():
        recommendations.append("Уникайте використання імені у паролі.")
    else:
        score += 2 # Не містить імені

    year = birth_date.split('.')[-1]
    if year in password :
        recommendations.append("Уникайте використання року народження у паролі.")
    else:
        score += 2 # Не містить рік

#Інші варіанти дати    
# month = birth_date.split('.')[1]
    # day = birth_date.split('.')[0]
    # if month in password or day in password:
    #     recommendations.append("Уникайте використання місяця або дня народження у паролі")

    # 2. Оцінювання складності
    length = len(password)
    if length >= 12:
        score += 3
    elif length >= 8:
        score += 1
    else:
        recommendations.append("Збільште довжину пароля (мінімум 8 символів, краще 12+).")

    # Різноманітність символів
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9\s]", password))

    if has_upper and has_lower and has_digit and has_symbol:
        score += 3
    elif (has_upper or has_lower) and has_digit:
        score += 1
    else:
        recommendations.append("Використовуйте великі та малі літери, цифри та спеціальні символи.")


    #Приклад простої перевірки на словникові слова (потрібна база даних для кращого аналізу)
    common_words = ["password", "qwerty", "123456"]
    password_lower = password.lower()
    for word in common_words:
        if word in password_lower:
            recommendations.append("Уникайте використання поширених слів у паролі.")
            break


    # Нормалізація оцінки
    score = min(score, 10)  # Максимальна оцінка - 10
    return score, recommendations


# Головна частина програми
if __name__ == "__main__":
    password = input("Введіть пароль: ")
    name = input("Введіть ваше ім'я: ")
    birth_date = input("Введіть вашу дату народження (DD.MM.YYYY): ")

    score, recommendations = analyze_password(password, name, birth_date)

    print("\nРезультати аналізу:")
    print(f"Оцінка безпеки: {score}/10")

    if recommendations:
        print("\nРекомендації:")
        for recommendation in recommendations:
            print(f"- {recommendation}")
    else:
        print("Пароль виглядає досить надійним (але завжди можна краще!).")
