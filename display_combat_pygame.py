import sys
import pygame
import logging

from mission import Mission

logging.basicConfig(level=logging.INFO)

def main():
    """Run the game."""

    # Initialize game and create a screen object.
    pygame.init()
    screen = pygame.display.set_mode((600,400))
    pygame.display.set_caption("Adorable Hopelessness")

    bg_color = (230, 230, 230)

    mission = Mission()
    stats = {'wins': 0, 'losses': 0}

    # Main game loop
    while True:

        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                run_combat(mission, stats)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run_combat(mission, stats)

        # Draw screen objects.
        screen.fill(bg_color)
        draw_results(screen, bg_color, mission)
        draw_stats(screen, bg_color, stats)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


def run_combat(mission, stats):
    """Run the combat mission."""
    mission.__init__()
    mission.resolve_combat()
    if mission.mission_success:
        stats['wins'] += 1
    else:
        stats['losses'] += 1


def draw_results(screen, bg_color, mission):
    """Draw the results of the last combat."""
    text_color = (0, 0, 0)
    font = pygame.font.SysFont(None, 48)
    screen_rect = screen.get_rect()

    if mission.mission_success is None:
        return
    elif mission.mission_success:
        result_msg = "Success! Avatar won."
    else:
        result_msg = "Failure! Avatar defeated."

    hp_msg = "Avatar HP: " + str(mission.avatar_hp)

    # Render result_msg and position slightly above center on the screen.
    result_msg_image = font.render(result_msg, True, text_color, bg_color)
    result_msg_image_rect = result_msg_image.get_rect()
    result_msg_image_rect.centerx = screen_rect.centerx
    result_msg_image_rect.bottom = screen_rect.centery - 5

    # Render hp_msg and position slightly below center on the screen.
    hp_msg_image = font.render(hp_msg, True, text_color, bg_color)
    hp_msg_image_rect = hp_msg_image.get_rect()
    hp_msg_image_rect.centerx = screen_rect.centerx
    hp_msg_image_rect.top = screen_rect.centery + 5

    # Draw message.
    screen.blit(result_msg_image, result_msg_image_rect)
    screen.blit(hp_msg_image, hp_msg_image_rect)


def draw_stats(screen, bg_color, stats):
    """Draw running statistics of wins and losses."""
    text_color = (100, 100, 100)
    font = pygame.font.SysFont(None, 32)

    # Render wins text and position in upper left corner.
    wins_image = font.render(
            "Wins: " + str(stats['wins']), True, text_color, bg_color)
    wins_image_rect = wins_image.get_rect()
    wins_image_rect.top = 10
    wins_image_rect.left = 10

    # Render losses text and position below wins.
    losses_image = font.render(
            "Losses: " + str(stats['losses']), True, text_color, bg_color)
    losses_image_rect = losses_image.get_rect()
    losses_image_rect.top = wins_image_rect.bottom + 5
    losses_image_rect.left = 10

    # Draw stats.
    screen.blit(wins_image, wins_image_rect)
    screen.blit(losses_image, losses_image_rect)


main()

