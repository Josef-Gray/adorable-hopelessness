import sys
import pygame
import logging
import re

import flags
from mission import Mission
from actor import Avatar

def run_combat(avatar, mission, stats):
    """Run the combat mission."""
    avatar.reset_hp()
    mission.enemy.reset_hp()
    mission_result = mission.resolve_combat(avatar)
    if mission_result is True:
        stats['wins'] += 1
    else:
        stats['losses'] += 1
    return mission_result


def draw_name_prompt(screen):
    """Draw the prompt for name input."""
    text_color = (0, 0, 0)
    font = pygame.font.SysFont(None, 36)
    screen_rect = screen.get_rect()

    msg = "Name your character:"

    # Render msg and position left of center on the screen.
    msg_image = font.render(msg, True, text_color)
    msg_image_rect = msg_image.get_rect()
    msg_image_rect.right = screen_rect.centerx - 10
    msg_image_rect.centery = screen_rect.centery

    # Draw message.
    screen.blit(msg_image, msg_image_rect)


def draw_name_input(screen, msg):
    """Draw the name being input."""
    text_color = (0, 0, 0)
    font = pygame.font.SysFont(None, 36)
    screen_rect = screen.get_rect()

    # Render msg and position right of center on the screen.
    msg_image = font.render(msg, True, text_color)
    msg_image_rect = msg_image.get_rect()
    msg_image_rect.left = screen_rect.centerx + 10
    msg_image_rect.centery = screen_rect.centery

    # Draw message.
    screen.blit(msg_image, msg_image_rect)


def draw_ready_question(screen):
    """Draw the prompt for game readiness."""
    text_color = (0, 0, 0)
    font = pygame.font.SysFont(None, 36)
    screen_rect = screen.get_rect()

    question = "Are you ready to adventure?"
    instruct = "Key SPACE to continue"

    # Render question and position in the center of the screen.
    question_image = font.render(question, True, text_color)
    question_image_rect = question_image.get_rect()
    question_image_rect.center = screen_rect.center

    # Render instruction and position at the center bottom of the
    # screen.
    instruct_image = font.render(instruct, True, text_color)
    instruct_image_rect = instruct_image.get_rect()
    instruct_image_rect.centerx = screen_rect.centerx
    instruct_image_rect.bottom = screen_rect.bottom - 10

    # Draw messages.
    screen.blit(question_image, question_image_rect)
    screen.blit(instruct_image, instruct_image_rect)


def draw_results(screen, avatar, mission_result):
    """Draw the results of the last combat."""
    text_color = (0, 0, 0)
    font = pygame.font.SysFont(None, 48)
    screen_rect = screen.get_rect()

    if mission_result is None:
        return
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

    # Draw stats.
    screen.blit(wins_image, wins_image_rect)
    screen.blit(losses_image, losses_image_rect)


def main():
    """Run the game."""
    flags.setup_flags("Adorable Hopelessness RPG.")

    # Initialize game and create a screen object.
    pygame.init()
    screen = pygame.display.set_mode((600,400))
    pygame.display.set_caption("Adorable Hopelessness")

    bg_color = (230, 230, 230)

    name_input = ''
    avatar = None

    # Game loop: Input avatar name
    while avatar is None:

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

        # Draw screen objects.
        screen.fill(bg_color)
        draw_name_prompt(screen)
        draw_name_input(screen, name_input)

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    # Game loop: Ready
    game_ready = False
    while not game_ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_ready = True
    
        # Draw screen objects.
        screen.fill(bg_color)
        draw_ready_question(screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    stats = {'wins': 0, 'losses': 0}
    mission = Mission()
    mission_result = run_combat(avatar, mission, stats)

    # Main game loop
    while True:

        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mission_result = run_combat(avatar, mission, stats)
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    mission_result = run_combat(avatar, mission, stats)

        # Draw screen objects.
        screen.fill(bg_color)
        draw_results(screen, avatar, mission_result)
        draw_stats(screen, stats)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


main()

