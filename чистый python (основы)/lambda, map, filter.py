# lambda func
names_list = ["Саша", "Маша", "Паша", "Лёша", "Дима", "Валера", "Лена", "Аркаша"]
lambda_string = lambda my_str: f"{my_str}!"


# map func
names_after_map = map(lambda_string, names_list)
print(list(names_after_map)) # ['Саша!', 'Маша!', 'Паша!', 'Лёша!', 'Дима!', 'Валера!', 'Лена!', 'Аркаша!']


# filter func
only_long_names = list(filter(lambda name: len(name) > 5, names_list))
print(only_long_names) # ['Валера', 'Аркаша']


# dataclass
from dataclasses import dataclass

@dataclass
class UsersData:
    name: str

users = [UsersData(user) for user in only_long_names]
for u in users:
    print(u.name)


# contextmanager
from contextlib import contextmanager


@contextmanager
def contextmanager_foo(name):
    print(f"Пришёл в гости к: {name}")
    yield
    print(f"Попрощался и ушёл.")

for u in users:
    with contextmanager_foo(u.name):
        print("Попил кофе")

"""
Пришёл в гости к: Валера
Попил кофе
Попрощался и ушёл.

Пришёл в гости к: Аркаша
Попил кофе
Попрощался и ушёл.
"""