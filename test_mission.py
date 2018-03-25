import unittest

import actor as a
import mission as m

class CombatBalanceTestCase(unittest.TestCase):
    """Tests for combat win and loss balance."""

    def test_player_l1_enemy_l1(self):
        """Test level 1 player vs level 1 enemy."""
        losses = 0
        retreats = 0
        runs = 10000
        player = a.Player()
        mission = m.Mission()

        for i in range(runs):
            player.heal()
            mission.__init__()
            mission_result = mission.resolve_combat(player)
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

    def test_player_wins(self):
        """Test player winning."""
        player = a.Player()
        mission = m.Mission()
        mission.enemy.hp = 1
        self.assertEqual(mission.resolve_combat(player), m.WIN)

    def test_player_loses(self):
        """Test player losing."""
        player = a.Player()
        mission = m.Mission()
        player.hp = 0
        self.assertEqual(mission.resolve_combat(player), m.LOSE)

