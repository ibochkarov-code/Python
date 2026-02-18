import random


def get_numbers_ticket(min_num: int, max_num: int, quantity: int) -> list:
    if (
        min_num < 1 or
        max_num > 1000 or
        min_num > max_num or
        quantity < 1 or
        quantity > (max_num - min_num + 1)
    ):
        return []

    numbers = random.sample(range(min_num, max_num + 1), quantity)
    return sorted(numbers)

try:
    min_num = int(input("Введіть мінімальне число (>=1): "))
    max_num = int(input("Введіть максимальне число (<=1000): "))
    quantity = int(input("Введіть кількість чисел: "))
    result = get_numbers_ticket(min_num, max_num, quantity)
    print(result)
except ValueError:
        print("Неправильний формат, введіть ціле число")




