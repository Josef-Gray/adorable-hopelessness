"""Classes for modeling game screens."""

import sys
import pygame

class Screen():
    """A representation of a game screen."""

    def __init__(self, bg_surface, bg_color):
        """Initialize screen attributes."""
        self.bg_surface = bg_surface
        self.bg_color = bg_color

        # Create screen in inactive state.
        self.active = False

    def catch_events(self):
        """Catch common events and include events for specific screens."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                self.catch_special_events(event)

    def display(self):
        """Draw and display the screen."""
        # Fill background color.
        self.bg_surface.fill(self.bg_color)

        # Draw objects.
        self.draw_objects()

        # Make the most recently drawn bg_surface visible.
        pygame.display.flip()

    def catch_special_events(self):
        """Overridable function for screen-specific events."""
        pass

    def draw_objects(self):
        """Overridable function for screen-specific objects."""
        pass

    def run(self):
        """Run the screen's game loop."""
        # Make the screen state active.
        self.active = True

        while self.active:
            # Check for events.
            self.catch_events()

            # Draw the screen.
            self.display()


class ReadyScreen(Screen):
    """The "ready to adventure" screen."""

    def __init__(self, bg_surface, bg_color):
        """Initialize screen attributes."""
        super().__init__(bg_surface, bg_color)

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.active = False

    def draw_objects(self):
        """Draw the prompt for game readiness."""
        bg_surface_rect = self.bg_surface.get_rect()

        # Render question and position in the center of bg_surface.
        ready = "Are you ready to adventure?"
        ready_text_color = (0, 0, 0)
        ready_font = pygame.font.SysFont(None, 36)
        ready_image = ready_font.render(ready, True, ready_text_color)
        ready_image_rect = ready_image.get_rect()
        ready_image_rect.center = bg_surface_rect.center

        # Render instruction and position at the center bottom of
        # bg_surface.
        inst = "Press SPACE to continue"
        inst_text_color = (100, 100, 100)
        inst_font = pygame.font.SysFont(None, 32)
        inst_image = inst_font.render(inst, True, inst_text_color)
        inst_image_rect = inst_image.get_rect()
        inst_image_rect.centerx = bg_surface_rect.centerx
        inst_image_rect.bottom = bg_surface_rect.bottom - 10

        # Draw messages.
        self.bg_surface.blit(ready_image, ready_image_rect)
        self.bg_surface.blit(inst_image, inst_image_rect)

