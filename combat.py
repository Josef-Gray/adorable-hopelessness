from random import randrange

# Initialize avatar attributes.
avatar_hp = 10
avatar_min_damage = 1
avatar_max_damage = 3

# Initialize enemy attributes.
enemy_hp = 10
enemy_min_damage = 1
enemy_max_damage = 2

print("Avatar: " + str(avatar_hp) + "HP, " + str(avatar_min_damage) +
        "-" + str(avatar_max_damage) + " damage")
print("Enemy:  " + str(enemy_hp) + "HP, " + str(avatar_min_damage) +
        "-" + str(enemy_max_damage) + " damage")

# Perform combat
while avatar_hp > 0 and enemy_hp > 0:
    # If the first round, 50% chance to skip the avatar's turn
    if avatar_hp == 10 and randrange(2) == 0:
        pass
    else:
        damage = randrange(avatar_min_damage, avatar_max_damage + 1)
        enemy_hp -= damage
        print("Avatar hits for " + str(damage) + ". Enemy " +
                str(enemy_hp) + " HP remaining.")

    if enemy_hp > 0:
        damage = randrange(enemy_min_damage, enemy_max_damage + 1)
        avatar_hp -= damage
        print("\tEnemy hits for " + str(damage) + ". Avatar " +
                str(avatar_hp) + " HP remaining.")

# HP can't be less than 0.
if avatar_hp < 0:
    avatar_hp = 0
if enemy_hp < 0:
    enemy_hp = 0

print("Avatar: " + str(avatar_hp) + "HP")
print("Enemy:  " + str(enemy_hp) + "HP")

# Report results.
if avatar_hp > 0:
    print("Success! Avatar wins.")
else:
    print("Failure! Avatar defeated.")

