import unittest
import logging

from actor import Avatar
from mission import Mission

class CombatBalanceTestCase(unittest.TestCase):
    """Tests for combat win and loss balance."""

    def test_avatar_l1_enemy_l1(self):
        """Test level 1 avatar vs level 1 enemy."""
        losses = 0
        runs = 10000
        avatar = Avatar()
        mission = Mission()

        for i in range(runs):
            avatar.heal()
            mission.__init__()
            if not mission.resolve_combat(avatar):
                losses += 1

        loss_ratio = losses / runs
        self.assertLessEqual(
                loss_ratio, 0.15, msg="Losses higher than 15%")
        self.assertGreaterEqual(
                loss_ratio, 0.1, msg="Losses lower than 10%")


class MissionTestCase(unittest.TestCase):
    """Tests for combat results."""

    def test_avatar_wins(self):
        """Test avatar winning."""
        avatar = Avatar()
        mission = Mission()
        mission.enemy.hp = 1
        self.assertTrue(mission.resolve_combat(avatar))

    def test_avatar_loses(self):
        """Test avatar losing."""
        avatar = Avatar()
        mission = Mission()
        avatar.hp = 1
        self.assertFalse(mission.resolve_combat(avatar))

