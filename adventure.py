"""Functions for running adventures and displaying intro and results."""

import sys
import pygame

from stats import draw_stats

def start_adventure(screen, bg_color, stats, avatar, mission):
    """Start a new adventure."""
    # Avatar and enemy start with full hp.
    avatar.heal()
    mission.enemy.heal()

    # Resolve combat result.
    mission_result = mission.resolve_combat(avatar)

    # Record statistics
    if mission_result is True:
        stats['wins'] += 1
    elif mission_result is False:
        stats['losses'] += 1
    else:
        stats['retreats'] += 1

    # Display mission results
    while True:

        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

        # Draw screen objects.
        screen.fill(bg_color)
        draw_stats(screen, stats)
        draw_results(screen, avatar, mission_result)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


def draw_results(screen, avatar, mission_result):
    """Draw the results of the last combat."""
    text_color = (0, 0, 0)
    font = pygame.font.SysFont(None, 48)
    screen_rect = screen.get_rect()

    if mission_result is None:
        result_msg = avatar.name + " withdrew."
    elif mission_result is True:
        result_msg = "Success! " + avatar.name + " won."
    else:
        result_msg = "Failure! " + avatar.name + " defeated."

    hp_msg = avatar.name + " HP: " + str(avatar.hp)

    # Render result_msg and position slightly above center on the screen.
    result_msg_image = font.render(result_msg, True, text_color)
    result_msg_image_rect = result_msg_image.get_rect()
    result_msg_image_rect.centerx = screen_rect.centerx
    result_msg_image_rect.bottom = screen_rect.centery - 5

    # Render hp_msg and position slightly below center on the screen.
    hp_msg_image = font.render(hp_msg, True, text_color)
    hp_msg_image_rect = hp_msg_image.get_rect()
    hp_msg_image_rect.centerx = screen_rect.centerx
    hp_msg_image_rect.top = screen_rect.centery + 5

    # Draw messages.
    screen.blit(result_msg_image, result_msg_image_rect)
    screen.blit(hp_msg_image, hp_msg_image_rect)

