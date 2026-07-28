# -----------------------------
# Player (Warrior)
# -----------------------------

player = {
    "name": "Warrior",
    "health": 100,
    "max_health": 100,
    "attack": 20,
    "defense": 5,
    "potions": 3,
    "gold": 0,
    "status": "Alive"
}

# -----------------------------
# Enemies
# -----------------------------

enemies = {
    "goblin_1": {
        "name": "Goblin 1",
        "health": 40,
        "attack": 8,
        "reward": 10
    },

    "goblin_2": {
        "name": "Goblin 2",
        "health": 50,
        "attack": 10,
        "reward": 15
    },

    "orc_1": {
        "name": "Orc 1",
        "health": 70,
        "attack": 15,
        "reward": 20
    },

    "orc_2": {
        "name": "Orc 2",
        "health": 80,
        "attack": 18,
        "reward": 25
    },

    "dragon": {
        "name": "Dragon",
        "health": 150,
        "attack": 30,
        "reward": 100
    }
}


# -----------------------------
# Welcome
# -----------------------------

print("⚔️ Welcome to Warrior vs Enemies ⚔️")
print("Defeat all enemies to win!\n")


# -----------------------------
# Game Loop
# -----------------------------

for enemy_key in enemies:

    enemy = enemies[enemy_key]

    print(f"\n🔥 A wild {enemy['name']} appeared!")

    while player["health"] > 0 and enemy["health"] > 0:

        print("\n----------------------------")
        print(f"Your Health : {player['health']}")
        print(f"Enemy Health: {enemy['health']}")
        print(f"Potions     : {player['potions']}")
        print("----------------------------")

        action = input("1. Attack\n2. Potion\nChoose: ")

        # -----------------------------
        # Attack
        # -----------------------------

        if action == "1":

            enemy["health"] -= player["attack"]

            if enemy["health"] < 0:
                enemy["health"] = 0

            print(f"\nYou attacked {enemy['name']}.")
            print(f"{enemy['name']} Health = {enemy['health']}")

            if enemy["health"] == 0:
                print(f"\n✅ {enemy['name']} Defeated!")
                player["gold"] += enemy["reward"]
                print(f"You earned {enemy['reward']} Gold.")
                break

            # Enemy attacks

            player["health"] -= enemy["attack"]

            if player["health"] < 0:
                player["health"] = 0

            print(f"{enemy['name']} attacked you!")
            print(f"Your Health = {player['health']}")

        # -----------------------------
        # Potion
        # -----------------------------

        elif action == "2":

            if player["potions"] > 0:

                player["health"] += 30

                if player["health"] > player["max_health"]:
                    player["health"] = player["max_health"]

                player["potions"] -= 1

                print("🧪 Potion Used!")
                print(f"Your Health = {player['health']}")
                print(f"Potions Left = {player['potions']}")

                # Enemy attacks after potion

                player["health"] -= enemy["attack"]

                if player["health"] < 0:
                    player["health"] = 0

                print(f"{enemy['name']} attacked you!")
                print(f"Your Health = {player['health']}")

            else:
                print("❌ No Potions Left!")

        else:
            print("Invalid Choice!")

        # -----------------------------
        # Player Dead
        # -----------------------------

        if player["health"] == 0:
            print("\n💀 GAME OVER")
            player["status"] = "Dead"
            break

    if player["status"] == "Dead":
        break


# -----------------------------
# Victory
# -----------------------------

if player["status"] == "Alive":

    print("\n🏆 Congratulations!")
    print("You defeated all enemies!")
    print(f"Gold Collected: {player['gold']}")