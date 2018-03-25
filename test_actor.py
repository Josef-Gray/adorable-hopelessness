import unittest

import actor

class ActorTestCase(unittest.TestCase):
    """Tests for Actor class."""

    def test_full_heal(self):
        """Test healing to full."""
        player = actor.Player()
        player.hp = 0
        player.heal()
        self.assertEqual(player.hp, player.max_hp)

    def test_partial_heal(self):
        """Test partial healing."""
        player = actor.Player()
        player.hp = 0
        heal_hp = int(player.max_hp / 2)
        player.heal(heal_hp)
        self.assertEqual(player.hp, heal_hp)

    def test_negative_heal(self):
        """Test damage from healing."""
        player = actor.Player()
        heal_hp = int(-1 * player.max_hp / 2)
        player.heal(heal_hp)
        self.assertEqual(player.hp, player.max_hp + heal_hp)

