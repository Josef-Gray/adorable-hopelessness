import sys
import pygame

import flags
from background import Background
from actor import Player
from stats import Statistics
from mission import MissionList
import screen

def main():
    """Run the game."""
    flags.init_flags("Adorable Hopelessness RPG.")

    # Initialize game and create a background surface object.
    pygame.init()
    bg = Background()
    pygame.display.set_caption("Adorable Hopelessness")

    # Set player name
    player = Player()
    screen.PlayerNameScreen(bg, player).run()

    # Initialize stats
    stats = Statistics()

    # Create mission list
    mission_list = MissionList()

    # Loop ready / results
    while True:
        # Ready to adventure?
        screen.ReadyScreen(bg, player).run()

        # Choose an adventure
        screen.AdventureMenuScreen(bg, mission_list).run()

        # Run adventure
        screen.AdventureResultScreen(bg, stats, player,
                mission_list.get_active_mission()).run()


main()

