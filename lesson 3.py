# Генераторы


def weapon_ammo_countdown(ammo):
    while ammo >= 0:
        yield ammo
        ammo -= 1


for ammo in weapon_ammo_countdown(30):
    print(f"Патронов осталось: {ammo}")


gen = weapon_ammo_countdown(3)
print(next(gen)) # 3
print(next(gen)) # 2
print(next(gen)) # 1