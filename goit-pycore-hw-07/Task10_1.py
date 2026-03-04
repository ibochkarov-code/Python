from collections import UserDict
from datetime import datetime, date, timedelta


def input_error(func):
    """Декоратор для обробки помилок введення користувача у handler-функціях."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct arguments please."
        except IndexError:
            return "Enter the required arguments."
        except KeyError:
            return "Contact not found."
    return inner


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту (обов'язкове поле)."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (10 цифр)."""

    def __init__(self, value: str):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """Клас для зберігання дня народження у форматі DD.MM.YYYY."""

    def __init__(self, value: str):
        try:
            # Перетворюємо рядок на datetime.date
            dt = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(dt)

    def __str__(self):
        # Красивий вивід дати у форматі DD.MM.YYYY
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Запис контакту: ім'я + телефони + (необов'язково) день народження."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        """Додає телефон до запису."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Видаляє телефон із запису."""
        phone_obj = self.find_phone(phone)
        if phone_obj is None:
            raise KeyError
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Замінює існуючий телефон на новий."""
        phone_obj = self.find_phone(old_phone)
        if phone_obj is None:
            raise KeyError
        phone_obj.value = Phone(new_phone).value

    def find_phone(self, phone: str):
        """Повертає Phone, якщо знайдено, інакше None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str) -> None:
        """Додає день народження контакту (тільки один)."""
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        bday_str = str(self.birthday) if self.birthday else "None"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bday_str}"


class AddressBook(UserDict):
    """Адресна книга: зберігає записи та керує ними."""

    def add_record(self, record: Record) -> None:
        """Додає запис у книгу. Ключ — ім'я контакту."""
        self.data[record.name.value] = record

    def find(self, name: str):
        """Знаходить запис за ім'ям. Повертає Record або None."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за ім'ям."""
        if name not in self.data:
            raise KeyError
        del self.data[name]

    def get_upcoming_birthdays(self):
        today = date.today()
        end_day = today + timedelta(days=7)
        result = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday: date = record.birthday.value

            # Формуємо день народження у поточному році
            bday_this_year = bday.replace(year=today.year)

            # Якщо вже минув у цьому році — беремо наступний рік
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)

            if today <= bday_this_year <= end_day:
                congrat_date = bday_this_year

                # Перенесення з вихідних на понеділок
                if congrat_date.weekday() == 5:      # Saturday
                    congrat_date += timedelta(days=2)
                elif congrat_date.weekday() == 6:    # Sunday
                    congrat_date += timedelta(days=1)

                result.append({
                    "name": record.name.value,
                    "congratulation_date": congrat_date.strftime("%Y.%m.%d")
                })

        # Сортуємо за датою привітання
        result.sort(key=lambda x: x["congratulation_date"])
        return result


def parse_input(user_input: str):
    """Розбирає введений рядок на команду та аргументи (без урахування регістру)."""
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    """Команда: phone <name> — показує телефони контакту."""
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.phones:
        return "No phone numbers for this contact."
    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(args, book: AddressBook):
    """Команда: all — показує всі контакти."""
    if args:
        raise ValueError
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    """Команда: add-birthday <name> <DD.MM.YYYY> — додає день народження."""
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    """Команда: show-birthday <name> — показує день народження."""
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return "Birthday not set."
    return str(record.birthday)


@input_error
def birthdays(args, book: AddressBook):
    """Команда: birthdays — список привітань на наступний тиждень."""
    if args:
        raise ValueError
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."

    lines = []
    for item in upcoming:
        lines.append(f"{item['name']}: {item['congratulation_date']}")
    return "\n".join(lines)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break

        if command == "":
            continue

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()