import unittest
import logging

import actor as a
import mission as m

class CombatBalanceTestCase(unittest.TestCase):
    """Tests for combat win and loss balance."""

    def test_avatar_l1_enemy_l1(self):
        """Test level 1 avatar vs level 1 enemy."""
        losses = 0
        retreats = 0
        runs = 10000
        avatar = a.Avatar()
        mission = m.Mission()

        for i in range(runs):
            avatar.heal()
            mission.__init__()
            mission_result = mission.resolve_combat(avatar)
            if mission_result == m.LOSE:
                losses += 1
            elif mission_result == m.RETREAT:
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
        avatar = a.Avatar()
        mission = m.Mission()
        mission.enemy.hp = 1
        self.assertEqual(mission.resolve_combat(avatar), m.WIN)

    def test_avatar_loses(self):
        """Test avatar losing."""
        avatar = a.Avatar()
        mission = m.Mission()
        avatar.hp = 0
        self.assertEqual(mission.resolve_combat(avatar), m.LOSE)

