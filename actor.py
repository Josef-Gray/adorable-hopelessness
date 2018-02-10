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
        self.retreat_ratio = 0
        self.heal()

    def log_properties(self):
        """Log debug information about character properties."""
        logging.debug("Name: " + self.name)
        logging.debug("HP: " + str(self.hp))
        logging.debug("Max HP: " + str(self.max_hp))
        logging.debug("Max damage: " + str(self.max_damage))
        logging.debug("Min damage: " + str(self.min_damage))

    def heal(self, hp=0):
        """Heal fully (default) or by fixed hp."""
        # Heal by fixed hp if given (hp can be negative)
        if hp != 0 and self.hp + hp <= self.max_hp:
            self.hp += hp
        # Otherwise heal to full
        else:
            self.hp = self.max_hp


class Avatar(Actor):
    """A representation of a player character."""

    def __init__(self, name='Avatar'):
        """Initialize character attributes."""
        super().__init__()
        self.name = name
        self.max_damage = 3
        self.retreat_ratio = 0.1


