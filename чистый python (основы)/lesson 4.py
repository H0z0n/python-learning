# Декоратор
import time


# Практика №1
def log_shot(func):
    def shot():
        print("--- Начало выстрела ---")
        func()
        print("--- Конец выстрела ---")
    return shot


@log_shot
def fire():
    print("Пиу!")

@log_shot
def fire_test():
    print("ПИУ-ПИУ!!")

fire()
fire_test()


# Практика №2
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        finish = time.time()
        print(f"Разница: {finish - start:.4f}")
    return wrapper


@timer
def count_to(n):
    time.sleep(0.5)

    for i in range(1, n + 1):
        print(i)


count_to(10)