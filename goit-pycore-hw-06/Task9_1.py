from collections import UserDict

def input_error(func):
    """Декоратор для обробки помилок введення користувача у handler-функціях."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
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


class Record:
    """Запис контакту: ім'я + список телефонів."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

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

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


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
    """
    Команда: add <name> <phone>
    Якщо запису немає — створюємо.
    Якщо запис є — додаємо телефон у список.
    """
    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_phone(phone)
    return "Contact added."


@input_error
def change_contact(args, book: AddressBook):

    name, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError

    if record.phones:
        old_phone = record.phones[0].value
        record.edit_phone(old_phone, new_phone)
    else:
        record.add_phone(new_phone)

    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):

    name = args[0]  # може кинути IndexError
    record = book.find(name)
    if record is None:
        raise KeyError

    if not record.phones:
        return "No phone numbers for this contact."

    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(args, book: AddressBook):
    """
    Команда: all
    Виводить усі контакти.
    """
    if args:
        raise ValueError

    if not book.data:
        return "No contacts saved."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def delete_contact(args, book: AddressBook):
    """Команда: delete <name>"""
    name = args[0]
    book.delete(name)
    return "Contact deleted."


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

        if command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "delete":
            print(delete_contact(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()