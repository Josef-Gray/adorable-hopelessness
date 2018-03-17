import sys
import pygame

import flags
import init
from adventure import choose_adventure, start_adventure
from mission import Mission

def main():
    """Run the game."""
    flags.init_flags("Adorable Hopelessness RPG.")

    # Initialize game and create a screen object.
    pygame.init()
    screen = pygame.display.set_mode((600,400))
    pygame.display.set_caption("Adorable Hopelessness")

    bg_color = (230, 230, 230)

    # Set player name
    avatar = init.set_player_name(screen, bg_color)

    stats = {'wins': 0, 'losses': 0, 'retreats': 0}

    # Create mission list
    missions = init.init_missions()

    # Loop ready / results
    while True:
        # Ready to adventure?
        init.player_ready(screen, bg_color)

        # Choose an adventure
        mission = choose_adventure(screen, bg_color, missions)

        # Run adventure
        start_adventure(screen, bg_color, stats, avatar, mission)


main()

