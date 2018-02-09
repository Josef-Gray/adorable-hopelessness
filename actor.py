"""Classes for modeling player and non-player characters."""

import logging

class Actor():
    """A representation of a game character."""

    def __init__(self, name='actor_name'):
        """Initialize character attributes."""
        # Set default attributes.
        self.name = name
        self.max_hp = 10
        self.min_damage = 1
        self.max_damage = 2
        self.reset_hp()

    def log_properties(self):
        """Log debug information about character properties."""
        logging.debug("Name: " + self.name)
        logging.debug("HP: " + str(self.hp))
        logging.debug("Max HP: " + str(self.max_hp))
        logging.debug("Max damage: " + str(self.max_damage))
        logging.debug("Min damage: " + str(self.min_damage))

    def reset_hp(self):
        self.hp = self.max_hp


class Avatar(Actor):
    """A representation of a player character."""

    def __init__(self, name='Avatar'):
        super().__init__()
        self.name = name
        self.max_damage = 3

