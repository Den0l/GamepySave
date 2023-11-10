import random
import json
import csv

# Список оружия
weapons = {
    "dagger": {"name": "Кинжал", "damage": random.randint(3, 7), "price": 10},
    "sword": {"name": "Меч", "damage": random.randint(5, 10), "price": 20},
    "axe": {"name": "Топор", "damage": random.randint(7, 12), "price": 30},
    "bow": {"name": "Лук", "damage": random.randint(8, 14), "price": 40},
    "magic_staff": {"name": "Посох", "damage": random.randint(10, 18), "price": 50},
}

# Словарь предметов
items = {
    "health_potion": {"name": "Health Potion", "heal": 20, "price": 10},
    "instakill_scroll": {"name": "Instakill Scroll", "description": "Мгновенное убийство врага", "price": 50},
    "revive_potion": {"name": "Revive Potion", "description": "Возрождение героя", "price": 30},
}


# Множество для инвентаря игрока
inventory = set()

# Характеристики игрока
player = {
    "name": "Hero",
    "hp": 100,
    "attack": 12,
    "defense": 5
}

heroes = [
    {"name": "Воин", "hp": 120, "attack": 15, "defense": 10},
    {"name": "Маг", "hp": 80, "attack": 20, "defense": 5},
    {"name": "Лучник", "hp": 100, "attack": 10, "defense": 8}
]

# Список доступных врагов
available_enemies = [
    {"name": "Гоблин", "hp": 30, "attack": 25},
    {"name": "Орк", "hp": 40, "attack": 20},
    {"name": "Дракон", "hp": 50, "attack": 35},
    {"name": "Паук", "hp": 20, "attack": 15},
    {"name": "Змея", "hp": 10, "attack": 10},
    {"name": "Мышь", "hp": 5, "attack": 5}
]

# Список текущих врагов (максимум 3)
current_enemies = []

# Функция для использования предметов
def use_item(item_key):
    if item_key in inventory:
        item = items.get(item_key)
        if item:
            if item_key == "health_potion":
                player['hp'] += item['heal']
                print(f"Вы использовали {item['name']} и восстановили {item['heal']} HP.")
            inventory.remove(item_key)
        else:
            print("Предмет не найден.")
    else:
        print("У вас нет такого предмета в инвентаре.")

# Функция для описания игрока
def describe_player(coins):
    print(f"{player['name']} (HP: {player['hp']}, Attack: {player['attack']}, Defense: {player['defense']}, Coins: {coins})")
    print("Инвентарь: ", ", ".join(inventory))


# Функция для атаки врага
def attack_enemy(enemy):
    damage = random.randint(0, player['attack'])
    enemy['hp'] = max(0, enemy['hp'] - damage)
    print(f"{player['name']} атаковали {enemy['name']} на {damage} дамага!")

# Функция для атаки игрока врагом
def enemy_attack_player(enemy):
    damage = random.randint(0, enemy['attack'])
    player['hp'] = max(0, player['hp'] - max(0, damage - player['defense']))
    print(f"{enemy['name']} атаковал {player['name']} на {damage} дамага!")

def create_enemy():
    if len(current_enemies) < 3:
        enemy_name = random.choice(available_enemies)
        enemy = {
            "name": enemy_name,
            "hp": random.randint(20, 50),
            "attack": random.randint(5, 15),
            "defense": random.randint(1, 5)
        }
        current_enemies.append(enemy)
        print(f"Появился новый враг: {enemy['name']} (HP: {enemy['hp']}, Attack: {enemy['attack']}, Defense: {enemy['defense']})")
        return enemy
    return None

def update_enemy_stats(enemy):
    enemy['hp'] += random.randint(5, 10)
    enemy['attack'] += random.randint(1, 3)
    enemy['defense'] += random.randint(1, 3)

def display_inventory():
    if inventory:
        print("Ваш инвентарь: " + ', '.join(inventory))
    else:
        print("Ваш инвентарь пуст.")

# Функция для битвы с врагами
def battle(coins, item_name):
    while current_enemies and player['hp'] > 0:
        describe_player(coins)
        print("Текущие враги:")
        for i, enemy in enumerate(current_enemies):
            print(f"{i + 1}. {enemy['name']} (HP: {enemy['hp']}, Attack: {enemy['attack']})")
        print("4. Магазин")
        print("5. Использовать предмет")
        choice = input("Выберите врага для атаки (1 to " + str(len(current_enemies)) + ") или введите 'Магазин' или 'Использовать предмет': ")

        if choice == "Выход":
            break
        elif choice.isdigit():
            enemy_index = int(choice) - 1
            if 0 <= enemy_index < len(current_enemies):
                enemy = current_enemies[enemy_index]
                attack_enemy(enemy)
                if enemy['hp'] <= 0:
                    coins += random.randint(1, 10)
                    inventory.add(item_name)
                    current_enemies.pop(enemy_index)
                    player['hp'] += random.randint(5, 10)
                    new_enemy = create_enemy()
                    if new_enemy:
                        enemy_attack_player(new_enemy)
                else:
                    enemy_attack_player(enemy)
            else:
                print("Не правильный выбор")
        elif choice.lower() == "магазин":
            coins, item_name = shop(coins)
        if choice.lower() == "использовать предмет":
            print("Выберите предмет для использования:")
            print("1. Зелье здоровья (q)")
            print("2. Мгновенное убийство (w)")
            print("3. Воскрешение (e)")
            item_choice = input("Введите номер предмета (q/w/e) или 'отмена' для возврата: ")
            
            if item_choice == "q":
                if "health_potion" in inventory:
                    player['hp'] += items['health_potion']['heal']
                    inventory.remove("health_potion")
                    print(f"Вы использовали {items['health_potion']['name']} и восстановили {items['health_potion']['heal']} HP. У вас осталось {', '.join(inventory)}.")
                else:
                    print("У вас нет зелья здоровья в инвентаре.")
            elif item_choice == "w":
                if current_enemies:
                    current_enemies.pop(0)
                    print(f"Вы использовали {items['instakill_scroll']['name']} и уничтожили первого врага.")
                else:
                    print(f"У вас нет врагов, чтобы использовать {items['instakill_scroll']['name']}.")
            elif item_choice == "e":
                if player['hp'] <= 0:
                    player['hp'] = 1
                    inventory.remove("revive_potion")
                    print(f"Вы использовали {items['revive_potion']['name']} и возродились с 1 HP. У вас осталось {', '.join(inventory)}.")
                else:
                    print(f"Вы не можете использовать {items['revive_potion']['name']} в данный момент.")
            elif item_choice.lower() == "отмена":
                continue  
            else:
                print("Неверный выбор предмета.")
        else:
            print("Не правильный выбор")
    display_inventory()
    return coins

data = {
    "Name"
    "Hero"
    "Inventory"
}

def savejson(data, filename):

    try:
        with open(filename + ".json", 'r', encoding='utf-8') as file:
            current_data = json.load(file)
    except FileNotFoundError:
        current_data = []
    
    current_data.append(data)
    
    with open(filename + ".json", "w", encoding='utf-8') as file:
        json.dump(current_data, file, ensure_ascii=False)

def savecsv(data, filename):
    try:
        with open(filename + ".csv", 'r', newline='') as file:
            reader = csv.reader(file)
            current_data = list(reader)
    except FileNotFoundError:
        current_data = []

    current_data.append(data.values())

    with open(filename + ".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(current_data)


# Функция для магазина
def shop(coins):
    item_name = ""
    while True:
        print("Добро пожаловать в магазин!")
        print("У вас есть", coins, "монет.")
        print("Доступные предметы:")
        for i, (item_name, item) in enumerate(items.items()):
            print(f"{i + 1}. {item['name']} (Цена: {item['price']} монет)")
        
        choice = input("Выберите предмет для покупки (1 to " + str(len(items)) + ") или введите 'выход': ")
        
        if choice == "выход":
            break
        elif choice.isdigit():
            item_index = int(choice) - 1
            if 0 <= item_index < len(items):
                item_name = list(items.keys())[item_index]
                item = items[item_name]
                if coins >= item['price']:
                    coins -= item['price']
                    if item_name == "health_potion":
                        player['hp'] += item['heal']
                        print(f"Вы использовали {item['name']} и восстановили {item['heal']} HP. У вас осталось {coins} монет.")
                    elif item_name == "instakill_scroll":
                        if current_enemies:
                            current_enemies.pop(0)
                            print(f"Вы использовали {item['name']} и уничтожили первого врага.")
                        else:
                            print(f"У вас нет врагов, чтобы использовать {item['name']}.")
                    elif item_name == "revive_potion":
                        if player['hp'] <= 0:
                            player['hp'] = 1 
                            print(f"Вы использовали {item['name']} и возродились с 1 HP.")
                        else:
                            print(f"Вы не можете использовать {item['name']} в данный момент.")
                else:
                    print("У вас недостаточно монет для покупки.")
            else:
                print("Не правильный выбор")
        else:
            print("Не правильный выбор")
    display_inventory()
    return coins, item_name


print("Выберите своего героя:")
for i, hero in enumerate(heroes):
    print(f"{i + 1}. {hero['name']} (HP: {hero['hp']}, Attack: {hero['attack']}, Defense: {hero['defense']})")

hero_choice = input("Введите номер выбранного героя (1 to 3): ")
if hero_choice.isdigit():
    hero_index = int(hero_choice) - 1
    if 0 <= hero_index < len(heroes):
        player = heroes[hero_index]
        print(f"Вы выбрали героя: {player['name']}")
    else:
        print("Неправильный выбор, будет выбран герой по умолчанию.")
else:
    print("Неправильный выбор, будет выбран герой по умолчанию.")


# Главная игровая петля
item_name = ""
coins = 0
while player['hp'] > 0:
    print("Вы просыпаетесь в подземелье ваши действия.")
    print("1. Прогулка по подземелью")
    print("2. Просмотр инвентаря")
    print("3. Выйти из игры.")
    choice = input("Сделайте выбор (1/2/3): ")

    if choice == "1":
        create_enemy()
        coins = battle(coins, item_name)  
    elif choice == "2":
        describe_player(coins)
    elif choice == "3":
        print("Вы вышли из игры")
        break
    else:
        print("Не правильный выбор")

print("Игра окончена")

data = {}


print("Напишите свое имя")
data["Name"] = input()
data["Hero"] = player
data["Inventory"] = list(inventory)
print("Напишите путь для сохранения файла.")
filename = input()
savejson(data, filename)
savecsv(data, filename)

    
