def input_error(func):
    """Декоратор для обробки помилок введення користувача у handler-функціях."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            # Наприклад: не вистачає аргументів для "add" або "change"
            return "Give me name and phone please."
        except IndexError:
            # Наприклад: не вказали ім'я для "phone"
            return "Enter user name."
        except KeyError:
            # Наприклад: контакту з таким ім'ям немає
            return "Contact not found."
    return inner


def parse_input(user_input: str):
    """Розбирає рядок користувача на команду та аргументи (без урахування регістру)."""
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


@input_error
def add_contact(args, contacts):
    """Додає контакт: add <name> <phone>."""
    name, phone = args  # може кинути ValueError
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    """Змінює номер: change <name> <phone>."""
    name, phone = args  # може кинути ValueError
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    """Показує телефон: phone <name>."""
    name = args[0]  # може кинути IndexError
    if name not in contacts:
        raise KeyError
    return contacts[name]


@input_error
def show_all(args, contacts):
    """Показує всі контакти: all."""
    # Якщо користувач передав зайві аргументи — вважаємо помилкою формату
    if args:
        raise ValueError

    if not contacts:
        return "No contacts saved."

    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "\n".join(lines)


def main():
    contacts = {}
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
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(args, contacts))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()