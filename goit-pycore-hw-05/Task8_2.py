import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:

    # Регулярний вираз для пошуку дійсних чисел, які відокремлені пробілами
    pattern = r"(?<=\s)\d+\.\d+(?=\s)"

    # Проходимо по всіх знайдених числах у тексті
    for match in re.finditer(pattern, text):
        # Перетворюємо знайдене число у тип float та повертаємо через yield
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    
    # Викликаємо передану функцію-генератор і підсумовуємо всі значення
    return sum(func(text))


# Приклад використання
if __name__ == "__main__":
    text = (
        "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, "
        "доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    )

    # Викликаємо функцію підрахунку прибутку
    total_income = sum_profit(text, generator_numbers)

    # Виводимо результат
    print(f"Загальний дохід: {total_income}")