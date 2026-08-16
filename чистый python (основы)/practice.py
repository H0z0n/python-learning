# Задача №1
class Car:
    def __init__(self, brand: str, speed: int) -> None:
        self.brand = brand
        self.speed = speed

    def accelerate(self, amount: int) -> None:
        self.speed += amount
        print(f"Текущая скорость: {self.speed} км/ч")

class SportCar(Car):
    def __init__(self, brand: str, speed: int, turbo_boost: int) -> None:
        super().__init__(brand, speed)
        self.turbo_boost = turbo_boost

    def accelerate(self, amount: int) -> None:
        super().accelerate(amount + self.turbo_boost)

my_new_car = Car("BMW", 150)
my_new_car.accelerate(50)

my_new_sport_car = SportCar("Lamborghini", 200, 100)
my_new_sport_car.accelerate(50)


# Задача №2
def even_numbers(limit: int):
    try:
        if limit < 0:
            print("Число должно быть >= 0")
            return

        for i in range(0, limit + 1):
            if i % 2 == 0:
                yield i
    except ValueError:
        print("Должно быть число!")

for i in even_numbers(10):
    print(i)


# Задача №3
def require_positive(func) -> None:
    def wrapper(*args):
        if args[0] < 0:
            print("Первый аргумент должен быть больше нуля!")
            return

        func(*args)
    return wrapper

@require_positive
def get_numbers(*n: tuple) -> None:
    print(*n)

get_numbers(-5, 20, 10)
get_numbers(100, -10, 0)


# Задача №4
import os


def save_scores_to_file(filepath: str, scores: dict) -> None:
    dict_items = scores.items()

    with open(filepath, "w", encoding="utf-8") as file:
        for item in dict_items:
            name, score = item
            file.write(f"{name}:{score}\n")


script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "score.txt")

save_scores_to_file(filepath, {"Sasha": 100, "Alice": 95, "Jack": 55, "Michal": 0})