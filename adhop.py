import sys
import pygame

import flags
import setup
from adventure import choose_adventure, start_adventure
from mission import Mission

def main():
    """Run the game."""
    flags.setup_flags("Adorable Hopelessness RPG.")

    # Initialize game and create a screen object.
    pygame.init()
    screen = pygame.display.set_mode((600,400))
    pygame.display.set_caption("Adorable Hopelessness")

    bg_color = (230, 230, 230)

    # Set player name
    avatar = setup.set_player_name(screen, bg_color)

    stats = {'wins': 0, 'losses': 0, 'retreats': 0}

    # Create mission list
    missions = setup.setup_missions()

    # Loop ready / results
    while True:
        # Ready to adventure?
        setup.player_ready(screen, bg_color)

        # Choose an adventure
        mission = choose_adventure(screen, bg_color, missions)

        # Run adventure
        start_adventure(screen, bg_color, stats, avatar, mission)


main()

