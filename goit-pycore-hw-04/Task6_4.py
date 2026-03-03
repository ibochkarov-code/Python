def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."


def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        return "Contact not found."
    contacts[name] = phone
    return "Contact updated."


def show_phone(args, contacts):
    name = args[0]
    if name not in contacts:
        return "Contact not found."
    return contacts[name]


def show_all(contacts):
    if not contacts:
        return "No contacts saved."
    lines = []
    for name, phone in contacts.items():
        lines.append(f"{name}: {phone}")
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

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            if len(args) != 2:
                print("Invalid command.")
            else:
                print(add_contact(args, contacts))

        elif command == "change":
            if len(args) != 2:
                print("Invalid command.")
            else:
                print(change_contact(args, contacts))

        elif command == "phone":
            if len(args) != 1:
                print("Invalid command.")
            else:
                print(show_phone(args, contacts))

        elif command == "all":
            if args:
                print("Invalid command.")
            else:
                print(show_all(contacts))

        elif command == "":
            continue

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()