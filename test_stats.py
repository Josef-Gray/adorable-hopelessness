import unittest

from stats import Statistics
import mission

class StatisticsTestCase(unittest.TestCase):
    """Tests for Statistics class."""

    def test_win(self):
        """Test recording a win statistic."""
        stats = Statistics()
        stats.update(mission.WIN)
        self.assertEqual(stats.wins, 1)

    def test_lose(self):
        """Test recording a loss statistic."""
        stats = Statistics()
        stats.update(mission.LOSE)
        self.assertEqual(stats.losses, 1)
        
    def test_retreat(self):
        """Test recording a retreat statistic."""
        stats = Statistics()
        stats.update(mission.RETREAT)
        self.assertEqual(stats.retreats, 1)

