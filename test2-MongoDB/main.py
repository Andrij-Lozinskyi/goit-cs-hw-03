from pymongo import MongoClient
from typing import List, Dict, Any
import sys
import random

class CatDatabaseManager:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        """Ініціалізація підключення до MongoDB"""
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client.cats_db
            self.collection = self.db.cats
            print("Успішно підключено до бази даних")
        except Exception as e:
            print(f"Помилка підключення до бази даних: {e}")
            sys.exit(1)
            
    def create_random_cat(self) -> None:
        """Створення кота з випадковим іменем"""
        cat_names = ["Мурзик", "Мурка", "Мурчик", "Кітпес", "Гарфілд", "Том"]
        features_list = ["ходить в капці", "дає себе гладити", "рудий", "смугастий"]
        
        name = random.choice(cat_names)
        age = random.randint(1, 15)
        features = random.sample(features_list, random.randint(2, 4))
        
        while self.collection.find_one({"name": name}):
            name = f"{random.choice(cat_names)}_{random.randint(1, 100)}"
        
        cat_data = {
            "name": name,
            "age": age,
            "features": features
        }
        
        result = self.collection.insert_one(cat_data)
        if result.inserted_id:
            print(f"\nСтворено нового кота:")
            print(f"Ім'я: {name}")
            print(f"Вік: {age}")
            print(f"Характеристики: {', '.join(features)}")
        else:
            print("Помилка при створенні кота")

    def show_all_cats(self) -> None:
        """Виведення всіх записів із колекції"""
        cats = list(self.collection.find())
        if not cats:
            print("База даних порожня")
            return
        
        print("\nСписок всіх котів:")
        for cat in cats:
            print(f"\nІм'я: {cat['name']}")
            print(f"Вік: {cat['age']}")
            print(f"Характеристики: {', '.join(cat['features'])}")

    def find_cat_by_name(self, name: str) -> None:
        """Пошук та виведення інформації про кота за ім'ям"""
        cat = self.collection.find_one({"name": name})
        if cat:
            print(f"\nЗнайдено кота:")
            print(f"Ім'я: {cat['name']}")
            print(f"Вік: {cat['age']}")
            print(f"Характеристики: {', '.join(cat['features'])}")
        else:
            print(f"Кота з ім'ям {name} не знайдено")

    def update_cat_age(self, name: str, new_age: int) -> None:
        """Оновлення віку кота за ім'ям"""
        result = self.collection.update_one(
            {"name": name},
            {"$set": {"age": new_age}}
        )
        if result.modified_count:
            print(f"Вік кота {name} оновлено на {new_age}")
        else:
            print(f"Кота з ім'ям {name} не знайдено")

    def add_feature(self, name: str, new_feature: str) -> None:
        """Додавання нової характеристики до списку features"""
        result = self.collection.update_one(
            {"name": name},
            {"$addToSet": {"features": new_feature}}
        )
        if result.modified_count:
            print(f"Характеристику '{new_feature}' додано до кота {name}")
        else:
            print(f"Кота з ім'ям {name} не знайдено")

    def delete_cat(self, name: str) -> None:
        """Видалення запису за ім'ям тварини"""
        result = self.collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"Кота {name} видалено з бази даних")
        else:
            print(f"Кота з ім'ям {name} не знайдено")

    def delete_all_cats(self) -> None:
        """Видалення всіх записів із колекції"""
        result = self.collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів з бази даних")

def main():
    manager = CatDatabaseManager()
    
    while True:
        print("\nМеню управління базою даних котів:")
        print("1. Створити випадкового кота")
        print("2. Показати всіх котів")
        print("3. Знайти кота за ім'ям")
        print("4. Оновити вік кота")
        print("5. Додати характеристику коту")
        print("6. Видалити кота")
        print("7. Видалити всіх котів")
        print("0. Вийти")

        choice = input("\nВиберіть опцію: ")

        if choice == "1":
            manager.create_random_cat()
            
        elif choice == "2":
            manager.show_all_cats()
        
        elif choice == "3":
            name = input("Введіть ім'я кота: ")
            manager.find_cat_by_name(name)
        
        elif choice == "4":
            name = input("Введіть ім'я кота: ")
            try:
                age = int(input("Введіть новий вік: "))
                manager.update_cat_age(name, age)
            except ValueError:
                print("Помилка: вік повинен бути числом")
        
        elif choice == "5":
            name = input("Введіть ім'я кота: ")
            feature = input("Введіть нову характеристику: ")
            manager.add_feature(name, feature)
        
        elif choice == "6":
            name = input("Введіть ім'я кота: ")
            manager.delete_cat(name)
        
        elif choice == "7":
            manager.delete_all_cats()
            print("Коти видалені!")
        
        elif choice == "0":
            break
        
        else:
            print("Невірний вибір. Спробуйте ще раз")

if __name__ == "__main__":
    main()