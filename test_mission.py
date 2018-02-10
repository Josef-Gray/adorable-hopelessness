import unittest
import logging

from actor import Avatar
from mission import Mission

class CombatBalanceTestCase(unittest.TestCase):
    """Tests for combat win and loss balance."""

    def test_avatar_l1_enemy_l1(self):
        """Test level 1 avatar vs level 1 enemy."""
        losses = 0
        retreats = 0
        runs = 10000
        avatar = Avatar()
        mission = Mission()

        for i in range(runs):
            avatar.heal()
            mission.__init__()
            mission_result = mission.resolve_combat(avatar)
            if mission_result is False:
                losses += 1
            elif mission_result is None:
                retreats += 1

        loss_ratio = losses / runs
        retreat_ratio = retreats / runs
#        print("\nLosses: " + str(loss_ratio)
#                + "\nRetreats: " + str(retreat_ratio))
        self.assertLessEqual(
                loss_ratio, 0.07, msg="Losses higher than 7%")
        self.assertGreaterEqual(
                loss_ratio, 0.06, msg="Losses lower than 6%")
        self.assertLessEqual(
                retreat_ratio, 0.19, msg="Retreats higher than 19%")
        self.assertGreaterEqual(
                retreat_ratio, 0.17, msg="Retreats lower than 17%")


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

