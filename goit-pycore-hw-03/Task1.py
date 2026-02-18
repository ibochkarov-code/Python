from datetime import datetime


def get_days_from_today(date: str) -> int:
    try:
        # Перетворюємо рядок у datetime-об'єкт
        given_date = datetime.strptime(date, "%Y-%m-%d").date()

        # Отримуємо поточну дату (без часу)
        today = datetime.today().date()

        # Різниця між датами
        delta = today - given_date

        return delta.days

    except ValueError:
        raise ValueError("Неправильний формат дати. Використовуйте формат 'YYYY-MM-DD'.")

user_date = input("Введіть дату у форматі YYYY-MM-DD --->  ")
delta_days = get_days_from_today(user_date)
print(f"Різниця {delta_days} днів")