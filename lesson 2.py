# мини-генератор в цикле + списки []

class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __str__(self):
        return f"{self.name} ({self.weight} кг)"

class Potion(Item):
    def __init__(self, name, weight, heal_amount):
        super().__init__(name, weight)
        self.heal_amount = heal_amount

    def use(self):
        print(f"Выпито зелье {self.name}, восстановлено {self.heal_amount} HP!")


class Inventory:
    def __init__(self, max_weight):
        self._items = []
        self._max_weight = max_weight

    def add_item(self, item):
        # sum(existing.weight for existing in self._items) + item.weight
        
        total_weight = 0
        for item_in_list in self._items:
            total_weight += item_in_list.weight
        total_weight += item.weight

        if total_weight > self._max_weight:
            print("Слишком тяжело!")
        else:
            self._items.append(item)
            print(f"{item.name} добавлен в инвентарь!")

    def show_all(self):
        for item in self._items:
            print(item)


some_item = Item("Меч", 5)
print(some_item)

some_potion = Potion("Зелье исцеления", 2, 10)
print(some_potion)
some_potion.use()

new_inventory = Inventory(10)
new_inventory.add_item(some_item)
new_inventory.add_item(some_potion)
new_inventory.add_item(some_item)

print("\nВсе предметы: ")
new_inventory.show_all()