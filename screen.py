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

    def run(self):
        """Run the screen's game loop."""
        # Make the screen state active.
        self.active = True

        while self.active:
            # Check for events.
            self.catch_events()

            # Draw the screen.
            self.display()

    def display(self):
        """Draw and display the screen."""
        # Fill background color.
        self.bg_surface.fill(self.bg_color)

        # Draw objects.
        self.draw_objects()

        # Make the most recently drawn bg_surface visible.
        pygame.display.flip()

    def catch_events(self):
        """Catch common events and include events for specific screens."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                self.catch_special_events(event)

    def press_any_key(self, event):
        """Standard event catcher for "press any key to continue"."""
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self.active = False

    def catch_special_events(self, event):
        """Overridable function for screen-specific events."""
        pass

    def draw_objects(self):
        """Overridable function for screen-specific objects."""
        pass


class ReadyScreen(Screen):
    """The "ready to adventure" screen."""

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        self.press_any_key(event)

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


class AdventureResultScreen(Screen):
    """The adventure result screen."""

    def __init__(self, bg_surface, bg_color, stats, avatar, mission):
        super().__init__(bg_surface, bg_color)
        self.stats = stats
        self.avatar = avatar
        self.mission = mission

        # Avatar and enemy start with full hp.
        self.avatar.heal()
        self.mission.enemy.heal()

        # Resolve combat result.
        self.mission.resolve_combat(avatar)

        # Record statistics
        if self.mission.result is True:
            self.stats['wins'] += 1
        elif self.mission.result is False:
            self.stats['losses'] += 1
        else:
            self.stats['retreats'] += 1

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        self.press_any_key(event)

    def draw_objects(self):
        """Draw screen objects."""
        self.draw_results()
        self.draw_stats()

    def draw_results(self):
        """Draw the results of the last combat."""
        text_color = (0, 0, 0)
        title_font = pygame.font.SysFont(None, 42)
        result_font = pygame.font.SysFont(None, 36)
        bg_surface_rect = self.bg_surface.get_rect()

        if self.mission.result is None:
            result_msg = self.avatar.name + " withdrew."
        elif self.mission.result is True:
            result_msg = "Success! " + self.avatar.name + " won."
        else:
            result_msg = "Failure! " + self.avatar.name + " defeated."

        hp_msg = self.avatar.name + " HP: " + str(self.avatar.hp)

        # Render mission title and position slightly above center on bg_surface.
        title_msg_image = title_font.render(self.mission.title, True, text_color)
        title_msg_image_rect = title_msg_image.get_rect()
        title_msg_image_rect.centerx = bg_surface_rect.centerx
        title_msg_image_rect.bottom = bg_surface_rect.centery - 5

        # Render result_msg and position slightly below center on bg_surface.
        result_msg_image = result_font.render(result_msg, True, text_color)
        result_msg_image_rect = result_msg_image.get_rect()
        result_msg_image_rect.centerx = bg_surface_rect.centerx
        result_msg_image_rect.top = bg_surface_rect.centery + 5

        # Render hp_msg and position below result_msg on bg_surface.
        hp_msg_image = result_font.render(hp_msg, True, text_color)
        hp_msg_image_rect = hp_msg_image.get_rect()
        hp_msg_image_rect.centerx = bg_surface_rect.centerx
        hp_msg_image_rect.top = result_msg_image_rect.bottom + 5

        # Draw messages.
        self.bg_surface.blit(title_msg_image, title_msg_image_rect)
        self.bg_surface.blit(result_msg_image, result_msg_image_rect)
        self.bg_surface.blit(hp_msg_image, hp_msg_image_rect)

    def draw_stats(self):
        """Draw running statistics of wins and losses."""
        text_color = (100, 100, 100)
        font = pygame.font.SysFont(None, 32)

        # Render wins text and position in upper left corner.
        wins_image = font.render(
                "Wins: " + str(self.stats['wins']), True, text_color)
        wins_image_rect = wins_image.get_rect()
        wins_image_rect.top = 10
        wins_image_rect.left = 10

        # Render losses text and position below wins.
        losses_image = font.render(
                "Losses: " + str(self.stats['losses']), True, text_color)
        losses_image_rect = losses_image.get_rect()
        losses_image_rect.top = wins_image_rect.bottom + 5
        losses_image_rect.left = 10

        # Render retreats text and position below wins.
        retreats_image = font.render(
                "Retreats: " + str(self.stats['retreats']), True, text_color)
        retreats_image_rect = retreats_image.get_rect()
        retreats_image_rect.top = losses_image_rect.bottom + 5
        retreats_image_rect.left = 10

        # Draw stats.
        self.bg_surface.blit(wins_image, wins_image_rect)
        self.bg_surface.blit(losses_image, losses_image_rect)
        self.bg_surface.blit(retreats_image, retreats_image_rect)

