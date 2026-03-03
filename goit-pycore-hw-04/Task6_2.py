def get_cats_info(path):
    cats = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Пропускаємо порожні рядки
                if not line:
                    continue

                try:
                    cat_id, name, age = line.split(",")

                    cat_info = {
                        "id": cat_id,
                        "name": name,
                        "age": age
                    }

                    cats.append(cat_info)

                except ValueError:
                    print(f"Некоректный формат рядка: {line}")

        return cats

    except FileNotFoundError:
        print("Файл не знайдено.")
        return []
    except Exception as e:
        print(f"Помилка при обробці файлу: {e}")
        return []

cats_info = get_cats_info(r"C:\Users\38093\OneDrive\Рабочий стол\Python Learning Projects\cats.txt")
print(cats_info)