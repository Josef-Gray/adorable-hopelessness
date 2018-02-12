"""Functions for displaying win/loss statistics."""

import pygame

def draw_stats(screen, stats):
    """Draw running statistics of wins and losses."""
    text_color = (100, 100, 100)
    font = pygame.font.SysFont(None, 32)

    # Render wins text and position in upper left corner.
    wins_image = font.render(
            "Wins: " + str(stats['wins']), True, text_color)
    wins_image_rect = wins_image.get_rect()
    wins_image_rect.top = 10
    wins_image_rect.left = 10

    # Render losses text and position below wins.
    losses_image = font.render(
            "Losses: " + str(stats['losses']), True, text_color)
    losses_image_rect = losses_image.get_rect()
    losses_image_rect.top = wins_image_rect.bottom + 5
    losses_image_rect.left = 10

    # Render retreats text and position below wins.
    retreats_image = font.render(
            "Retreats: " + str(stats['retreats']), True, text_color)
    retreats_image_rect = retreats_image.get_rect()
    retreats_image_rect.top = losses_image_rect.bottom + 5
    retreats_image_rect.left = 10

    # Draw stats.
    screen.blit(wins_image, wins_image_rect)
    screen.blit(losses_image, losses_image_rect)
    screen.blit(retreats_image, retreats_image_rect)

