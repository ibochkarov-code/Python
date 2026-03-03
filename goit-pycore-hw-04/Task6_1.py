def total_salary(path):
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Пропускаємо порожні рядки
                if not line:
                    continue

                try:
                    name, salary = line.split(",")
                    total += float(salary)
                    count += 1
                except ValueError:
                    print(f"Некоректний формат рядка: {line}")

        if count == 0:
            return (0, 0)

        average = total / count
        return (total, average)

    except FileNotFoundError:
        print("Файл не знайдено.")
        return (0, 0)
    except Exception as e:
        print(f"Помилка при обробці файлу: {e}")
        return (0, 0)

salary_data = total_salary(r"C:\Users\38093\OneDrive\Рабочий стол\Python Learning Projects\salary.txt")
print(f"Загальна сума заробітної плати: {salary_data[0]}")
print(f"Середня заробітна плата: {salary_data[1]}")

