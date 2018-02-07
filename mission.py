"""Classes for modeling combat missions."""

import logging
from random import randrange

class Mission():
    """A representation of a combat mission."""

    def __init__(self):
        """Initialize mission attributes."""
        # Initialize mission_success with no result.
        self.mission_success = None

        # Initialize avatar attributes.
        self.avatar_hp = 10
        self.avatar_min_damage = 1
        self.avatar_max_damage = 3
        logging.info(
                "Avatar: " + str(self.avatar_hp) + "HP, "
                + str(self.avatar_min_damage) + "-"
                + str(self.avatar_max_damage) + " damage")

        # Initialize enemy attributes.
        self.enemy_hp = 10
        self.enemy_min_damage = 1
        self.enemy_max_damage = 2
        logging.info(
                "Enemy:  " + str(self.enemy_hp) + "HP, "
                + str(self.avatar_min_damage) + "-"
                + str(self.enemy_max_damage) + " damage")

    def resolve_combat(self):
        """Resolve combat and store result as mission_success."""
        # Perform combat
        while self.avatar_hp > 0 and self.enemy_hp > 0:
            # If the first round, 50% chance to skip the avatar's turn
            if self.avatar_hp == 10 and randrange(2) == 0:
                pass
            else:
                damage = randrange(
                        self.avatar_min_damage, self.avatar_max_damage + 1)
                self.enemy_hp -= damage
                logging.info("Avatar hits for " + str(damage) + ". "
                        + "Enemy " + str(self.enemy_hp) + " HP remaining.")

            if self.enemy_hp > 0:
                damage = randrange(
                        self.enemy_min_damage, self.enemy_max_damage + 1)
                self.avatar_hp -= damage
                logging.info("\tEnemy hits for " + str(damage) + ". " +
                        "Avatar " + str(self.avatar_hp) + " HP remaining.")

        # HP can't be less than 0.
        if self.avatar_hp < 0:
            self.avatar_hp = 0
        if self.enemy_hp < 0:
            self.enemy_hp = 0

        logging.info("Avatar: " + str(self.avatar_hp) + "HP")
        logging.info("Enemy:  " + str(self.enemy_hp) + "HP")

        # Report results.
        if self.avatar_hp > 0:
            self.mission_success = True
            logging.info("Success! Avatar wins.")
        else:
            self.mission_success = False
            logging.info("Failure! Avatar defeated.")


logging.basicConfig(level=logging.INFO)
mission = Mission()
mission.resolve_combat()
print(mission.mission_success)

