# Классы, наследование, ООП, try + expect
# Type hints (аннотации типов)
# +Работа с файлами

class Weapon:
    def __init__(self, name: str, ammo: int) -> None:
        self.name = name
        self._ammo = ammo

    def shoot(self) -> None:
        if self._ammo > 0:
            self._ammo -= 1
            print(f"Вы выстрелили из оружия {self.name}, осталось патронов: {self._ammo}")
        else:
            print("У вас закончились патроны!")
    
    def reload(self, amount: int) -> None:
        new_total = self._ammo + amount

        if new_total > 30:
            self._ammo = 30
            print("Магазин полон! Лишние патроны выброшены!")
        else:
            self._ammo = new_total

    def reload_from_input(self) -> None:
        custom_amount = input("Сколько зарядить патронов?")

        try:
            amount = int(custom_amount)
        except ValueError:
            print("Ошибка: нужно ввести число!")
            return

        if amount < 0:
            print("Ошибка: нельзя перезарядить отрицательным количеством!")
            return

        self.reload(amount)

    def get_ammo(self) -> int:
        return self._ammo


class Pistol(Weapon):
    pass


class Shotgun(Weapon):
    def __init__(self, name: str, ammo: int, pellets: int) -> None:
        super().__init__(name, ammo)
        self.pellets = pellets

    def shoot(self) -> None:
        super().shoot()
        print(f"Выстрел дробью! {self.pellets} дробинок разлетелось!")   


def load_weapons_from_file(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as file:
        weapons: list = []

        for line in file:
            line = line.strip()
            name, ammo = line.split(":")
            ammo = int(ammo)

            weapon = Weapon(name, ammo)
            weapons.append(weapon)

    return weapons
            

# myPistol = Pistol("Deagle", 7)
# myPistol.shoot()
# myPistol.reload_from_input()

# myShotgun = Shotgun("MAG-7", 10, 8)
# myShotgun.shoot()
# myShotgun.reload(15)

# weapons: list = []
weapons: list = load_weapons_from_file("weapons.txt")

for weapon in weapons:
    weapon.shoot()