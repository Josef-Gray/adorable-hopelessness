import sys
import pygame
import re
from random import choice

from actor import Avatar
from mission import Mission

def init_missions():
    """Return list of missions."""
    # Create mission list
    missions = []
    missions.append(Mission('Slay the Rat', 'Rat'))

    titles = ['Storm the Castle']
    enemies = ['Goblin']
    missions.append(Mission(choice(titles), choice(enemies)))

    return missions


def draw_name_prompt(bg_surface):
    """Draw the prompt for name input."""
    text_color = (0, 0, 0)
    font = pygame.font.SysFont(None, 36)
    bg_surface_rect = bg_surface.get_rect()

    msg = "Name your character:"

    # Render msg and position left of center on bg_surface.
    msg_image = font.render(msg, True, text_color)
    msg_image_rect = msg_image.get_rect()
    msg_image_rect.right = bg_surface_rect.centerx - 10
    msg_image_rect.centery = bg_surface_rect.centery

    # Draw message.
    bg_surface.blit(msg_image, msg_image_rect)


def draw_name_input(bg_surface, msg):
    """Draw the name being input."""
    text_color = (0, 0, 0)
    font = pygame.font.SysFont(None, 36)
    bg_surface_rect = bg_surface.get_rect()

    # Render msg and position right of center on bg_surface.
    msg_image = font.render(msg, True, text_color)
    msg_image_rect = msg_image.get_rect()
    msg_image_rect.left = bg_surface_rect.centerx + 10
    msg_image_rect.centery = bg_surface_rect.centery

    # Draw message.
    bg_surface.blit(msg_image, msg_image_rect)


def set_player_name(bg_surface, bg_color):
    """Set player name.

    Returns:
        The player avatar
    """
    name_input = ''

    while True:
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # If a "word" character, append to input
                if re.match(r'\w', event.unicode):
                    name_input += event.unicode
                # Backspace deletes the last letter
                elif event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                # Return ends name input and creates avatar
                elif event.key == pygame.K_RETURN:
                    avatar = Avatar(name_input)
                    avatar.log_properties()
                    return avatar

        # Draw objects.
        bg_surface.fill(bg_color)
        draw_name_prompt(bg_surface)
        draw_name_input(bg_surface, name_input)

        # Make the most recently drawn bg_surface visible.
        pygame.display.flip()

