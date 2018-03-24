import unittest

import actor

class ActorTestCase(unittest.TestCase):
    """Tests for Actor class."""

    def test_full_heal(self):
        """Test healing to full."""
        avatar = actor.Avatar()
        avatar.hp = 0
        avatar.heal()
        self.assertEqual(avatar.hp, avatar.max_hp)

    def test_partial_heal(self):
        """Test partial healing."""
        avatar = actor.Avatar()
        avatar.hp = 0
        heal_hp = int(avatar.max_hp / 2)
        avatar.heal(heal_hp)
        self.assertEqual(avatar.hp, heal_hp)

    def test_negative_heal(self):
        """Test damage from healing."""
        avatar = actor.Avatar()
        heal_hp = int(-1 * avatar.max_hp / 2)
        avatar.heal(heal_hp)
        self.assertEqual(avatar.hp, avatar.max_hp + heal_hp)

