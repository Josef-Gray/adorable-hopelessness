"""Classes for managing background surfaces."""

import pygame

class Background():
    """A representation of the background surface."""

    def __init__(self, resolution=(600,400), color=(230,230,230)):
        self.surface = pygame.display.set_mode(resolution)
        self.color = color

