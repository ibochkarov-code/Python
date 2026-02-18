from datetime import datetime, date, timedelta


def get_upcoming_birthdays(users: list) -> list:

    today = datetime.today().date()
    end_date = today + timedelta(days=7)

    upcoming = []

    for user in users:
        try:
            birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        except (KeyError, ValueError, TypeError):
            # Якщо немає ключа або неправильний формат дати — пропускаємо запис
            continue

        # День народження в поточному році
        birthday_this_year = birthday.replace(year=today.year)

        # Якщо вже минув — беремо наступний рік
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # Перевіряємо, чи потрапляє у вікно [today, today + 7]
        if today <= birthday_this_year <= end_date:
            congratulation_date = birthday_this_year

            # Перенос з вихідних на понеділок
            # weekday(): 0=Пн ... 5=Сб ... 6=Нд
            if congratulation_date.weekday() == 5:       # Saturday
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:     # Sunday
                congratulation_date += timedelta(days=1)

            upcoming.append({
                "name": user.get("name", ""),
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })

    return upcoming

#Приклад використання
users = [
    {"name": "John Doe", "birthday": "1985.01.23"},
    {"name": "Jane S", "birthday": "1991.01.27"},
    {"name": "Jane A", "birthday": "1992.02.20"},
    {"name": "Jane B", "birthday": "1993.02.21"},
    {"name": "Jane C", "birthday": "1994.02.16"},
    {"name": "Jane C", "birthday": "1995.02.26"}
]

birthdays = get_upcoming_birthdays(users)
print(birthdays)