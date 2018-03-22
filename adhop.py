import sys
import pygame

import flags
import init
import screen
from adventure import choose_adventure, start_adventure
from mission import Mission

def main():
    """Run the game."""
    flags.init_flags("Adorable Hopelessness RPG.")

    # Initialize game and create a background surface object.
    pygame.init()
    bg_surface = pygame.display.set_mode((600,400))
    pygame.display.set_caption("Adorable Hopelessness")

    bg_color = (230, 230, 230)

    # Set player name
    avatar = init.set_player_name(bg_surface, bg_color)

    stats = {'wins': 0, 'losses': 0, 'retreats': 0}

    # Create mission list
    missions = init.init_missions()

    # Loop ready / results
    while True:
        # Ready to adventure?
        screen.ReadyScreen(bg_surface, bg_color).run()

        # Choose an adventure
        mission = choose_adventure(bg_surface, bg_color, missions)

        # Run adventure
        #start_adventure(bg_surface, bg_color, stats, avatar, mission)
        screen.AdventureResultScreen(bg_surface, bg_color, stats,
                avatar, mission).run()


main()

