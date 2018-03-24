"""Classes for displaying win/loss statistics."""

import pygame
import mission

class Statistics():
    """Win and loss statistics."""

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.retreats = 0

    def update(self, mission_result):
        if mission_result == mission.WIN:
            self.wins += 1
        elif mission_result == mission.LOSE:
            self.losses += 1
        else:
            self.retreats += 1

    def draw(self, bg):
        """Draw running statistics of wins and losses."""
        text_color = (100, 100, 100)
        font = pygame.font.SysFont(None, 32)

        # Render wins text and position in upper left corner.
        wins_image = font.render(
                "Wins: " + str(self.wins), True, text_color)
        wins_image_rect = wins_image.get_rect()
        wins_image_rect.top = 10
        wins_image_rect.left = 10

        # Render losses text and position below wins.
        losses_image = font.render(
                "Losses: " + str(self.losses), True, text_color)
        losses_image_rect = losses_image.get_rect()
        losses_image_rect.top = wins_image_rect.bottom + 5
        losses_image_rect.left = 10

        # Render retreats text and position below wins.
        retreats_image = font.render(
                "Retreats: " + str(self.retreats), True, text_color)
        retreats_image_rect = retreats_image.get_rect()
        retreats_image_rect.top = losses_image_rect.bottom + 5
        retreats_image_rect.left = 10

        # Draw stats.
        bg.surface.blit(wins_image, wins_image_rect)
        bg.surface.blit(losses_image, losses_image_rect)
        bg.surface.blit(retreats_image, retreats_image_rect)

