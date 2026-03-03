def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        # Базові випадки
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # Перевіряємо кеш
        if n in cache:
            return cache[n]

        # Обчислюємо та зберігаємо в кеш
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)

        return cache[n]

    return fibonacci


fib = caching_fibonacci()

# Перевірка
print(fib(10))  # 55
print(fib(15))  # 610