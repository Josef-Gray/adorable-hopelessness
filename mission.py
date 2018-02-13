"""Classes for modeling combat missions."""

import logging
from random import randrange, shuffle
from itertools import cycle

import flags
from actor import Actor, Avatar

class Mission():
    """A representation of a combat mission."""

    def __init__(self, title='Title', enemy_name='Enemy'):
        """Initialize mission attributes."""
        # Set the title.
        self.title = title

        # Create an enemy.
        self.enemy = Actor(enemy_name)
        self.enemy.log_properties()

        # Default result is None.
        self.result = None

    def resolve_combat(self, avatar):
        """Resolve combat.
        
        Args:
            avatar: The player character.
            
        Returns:
            (bool) True if avatar wins, false if avatar loses.
        """
        # Randomize whether avatar or enemy hits first.
        actors = [avatar, self.enemy]
        shuffle(actors)

        # Perform combat
        for i in cycle(range(2)):
            # End combat if actor has hp less than retreat ratio
            if actors[i].hp <= actors[i].max_hp * actors[i].retreat_ratio:
                break
            damage = randrange(
                    actors[i].min_damage, actors[i].max_damage + 1)
            actors[i-1].hp -= damage
            logging.debug(
                    actors[i].name + " hits for " + str(damage) + ". "
                    + actors[i-1].name + " " + str(actors[i-1].hp)
                    + " HP remaining.")

        logging.debug(avatar.name + ": " + str(avatar.hp) + "HP")
        logging.debug(self.enemy.name + ":  " + str(self.enemy.hp) + "HP")

        # Report results.
        if self.enemy.hp <= 0:
            logging.info(avatar.name + " won.")
            self.result = True
        elif avatar.hp > 0:
            logging.info(avatar.name + " withdrew.")
            self.result = None
        else:
            avatar.hp = 0
            logging.info(avatar.name + " defeated.")
            self.result = False

        return self.result


# Execute this only if running as a standalone
if __name__ == "__main__":
    flags.setup_flags("Combat mission test module.")
    avatar = Avatar()
    mission = Mission()
    logging.debug(mission.resolve_combat(avatar))

