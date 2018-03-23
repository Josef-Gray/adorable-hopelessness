import sys
import pygame

import flags
from actor import Avatar
from stats import Statistics
from mission import MissionList
import screen

def main():
    """Run the game."""
    flags.init_flags("Adorable Hopelessness RPG.")

    # Initialize game and create a background surface object.
    pygame.init()
    bg_surface = pygame.display.set_mode((600,400))
    pygame.display.set_caption("Adorable Hopelessness")

    bg_color = (230, 230, 230)

    # Set player name
    avatar = Avatar()
    screen.PlayerNameScreen(bg_surface, bg_color, avatar).run()

    # Initialize stats
    stats = Statistics()

    # Create mission list
    mission_list = MissionList()

    # Loop ready / results
    while True:
        # Ready to adventure?
        screen.ReadyScreen(bg_surface, bg_color).run()

        # Choose an adventure
        screen.AdventureMenuScreen(bg_surface, bg_color,
                mission_list).run()

        # Run adventure
        screen.AdventureResultScreen(bg_surface, bg_color, stats,
                avatar, mission_list.get_active_mission()).run()


main()

