"""Classes for modeling combat missions."""

import logging
from random import randrange

from actor import Avatar

class Mission():
    """A representation of a combat mission."""

    def __init__(self):
        """Initialize mission attributes."""
        # Initialize mission_success with no result.
        self.mission_success = None

        # Initialize enemy attributes.
        self.enemy_hp = 10
        self.enemy_min_damage = 1
        self.enemy_max_damage = 2
        logging.debug(
                "Enemy:  " + str(self.enemy_hp) + "HP, "
                + str(self.enemy_min_damage) + "-"
                + str(self.enemy_max_damage) + " damage")

    def resolve_combat(self, avatar):
        """Resolve combat and store result as mission_success."""
        # Perform combat
        while avatar.hp > 0 and self.enemy_hp > 0:
            # If the first round, 50% chance to skip the avatar's turn
            if avatar.hp == 10 and randrange(2) == 0:
                pass
            else:
                damage = randrange(
                        avatar.min_damage, avatar.max_damage + 1)
                self.enemy_hp -= damage
                logging.debug("Avatar hits for " + str(damage) + ". "
                        + "Enemy " + str(self.enemy_hp) + " HP remaining.")

            if self.enemy_hp > 0:
                damage = randrange(
                        self.enemy_min_damage, self.enemy_max_damage + 1)
                avatar.hp -= damage
                logging.debug("\tEnemy hits for " + str(damage) + ". " +
                        "Avatar " + str(avatar.hp) + " HP remaining.")

        logging.debug("Avatar: " + str(avatar.hp) + "HP")
        logging.debug("Enemy:  " + str(self.enemy_hp) + "HP")

        # Report results.
        if avatar.hp > 0:
            self.mission_success = True
            logging.info("Success! Avatar won.")
        else:
            avatar.hp = 0
            self.mission_success = False
            logging.info("Failure! Avatar defeated.")


# Execute this only if running as a standalone
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    avatar = Avatar()
    mission = Mission()
    mission.resolve_combat(avatar)
    logging.debug(mission.mission_success)

