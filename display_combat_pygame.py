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

    if mission.mission_success is None:
        msg = ''
    elif mission.mission_success:
        msg = 'Success! Avatar won.'
    else:
        msg = 'Failure! Avatar defeated.'

    # Turn msg into a rendered image and center on the screen.
    msg_image = font.render(msg, True, text_color, bg_color)
    msg_image_rect = msg_image.get_rect()
    screen_rect = screen.get_rect()
    msg_image_rect.center = screen_rect.center

    # Draw message.
    screen.blit(msg_image, msg_image_rect)


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
    losses_image_rect.top = wins_image_rect.bottom + 10
    losses_image_rect.left = 10

    # Draw stats.
    screen.blit(wins_image, wins_image_rect)
    screen.blit(losses_image, losses_image_rect)


main()

