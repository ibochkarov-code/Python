import sys
from pathlib import Path
from colorama import Fore, Style, init


def print_tree(path: Path, prefix: str = "") -> None:
    """
    Prints directory tree starting from `path`.
    Directories are colored differently from files.
    """
    items = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

    for index, item in enumerate(items):
        is_last = index == len(items) - 1

        branch = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")

        if item.is_dir():
            print(prefix + branch + Fore.CYAN + f"📂 {item.name}" + Style.RESET_ALL)
            print_tree(item, next_prefix)
        else:
            print(prefix + branch + Fore.GREEN + f"📜 {item.name}" + Style.RESET_ALL)


def main() -> None:
    init(autoreset=True)

    if len(sys.argv) < 2:
        print("Usage: python <script_name>.py <path_to_directory>")
        sys.exit(1)

    dir_path = Path(sys.argv[1])

    if not dir_path.exists():
        print(Fore.RED + "Error: path does not exist." + Style.RESET_ALL)
        sys.exit(1)

    if not dir_path.is_dir():
        print(Fore.RED + "Error: path is not a directory." + Style.RESET_ALL)
        sys.exit(1)

    print(Fore.MAGENTA + f"📦 {dir_path.resolve().name}" + Style.RESET_ALL)
    print_tree(dir_path)


if __name__ == "__main__":
    main()