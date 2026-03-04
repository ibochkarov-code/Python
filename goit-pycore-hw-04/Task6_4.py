def parse_input(user_input: str):
    # Розбиваємо введений рядок на слова
    parts = user_input.strip().split()

    # Якщо користувач нічого не ввів
    if not parts:
        return "", []

    # Перше слово — команда, інші — аргументи
    cmd = parts[0].lower()
    args = parts[1:]

    return cmd, args


def add_contact(args, contacts):
    # Очікується команда: add <ім'я> <телефон>
    if len(args) != 2:
        return "Give me name and phone please."

    name, phone = args
    contacts[name] = phone
    return "Contact added."


def change_contact(args, contacts):
    # Очікується команда: change <ім'я> <новий телефон>
    if len(args) != 2:
        return "Give me name and phone please."

    name, phone = args

    # Перевіряємо чи існує контакт
    if name not in contacts:
        return "Contact not found."

    contacts[name] = phone
    return "Contact updated."


def show_phone(args, contacts):
    # Очікується команда: phone <ім'я>
    if len(args) != 1:
        return "Enter user name."

    name = args[0]

    # Перевіряємо чи існує контакт
    if name not in contacts:
        return "Contact not found."

    return contacts[name]


def show_all(args, contacts):
    # Команда all не повинна мати аргументів
    if len(args) != 0:
        return "Invalid command."

    # Якщо контактів немає
    if not contacts:
        return "No contacts saved."

    # Формуємо список усіх контактів
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main():
    # Словник для зберігання контактів
    contacts = {}

    print("Welcome to the assistant bot!")

    # Основний цикл роботи бота
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        # Команди завершення роботи
        if command in ("close", "exit"):
            print("Good bye!")
            break

        if command == "":
            continue

        if command == "hello":
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