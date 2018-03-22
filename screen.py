"""Classes for modeling game screens."""

import sys
import pygame

class Screen():
    """A representation of a game screen."""

    def __init__(self, bg_surface, bg_color):
        """Initialize screen attributes."""
        self.bg_surface = bg_surface
        self.bg_surface_rect = self.bg_surface.get_rect()
        self.bg_color = bg_color

        self.text_color = (0, 0, 0)
        self.title_font = pygame.font.SysFont(None, 42)
        self.basic_font = pygame.font.SysFont(None, 36)

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
        # Render question and position in the center of bg_surface.
        ready_msg = "Are you ready to adventure?"
        ready_image = self.basic_font.render(ready_msg, True, self.text_color)
        ready_image_rect = ready_image.get_rect()
        ready_image_rect.center = self.bg_surface_rect.center

        # Render instruction and position at the center bottom of
        # bg_surface.
        inst_msg = "Press SPACE to continue"
        inst_text_color = (100, 100, 100)
        inst_font = pygame.font.SysFont(None, 32)
        inst_image = inst_font.render(inst_msg, True, inst_text_color)
        inst_image_rect = inst_image.get_rect()
        inst_image_rect.centerx = self.bg_surface_rect.centerx
        inst_image_rect.bottom = self.bg_surface_rect.bottom - 10

        # Draw messages.
        self.bg_surface.blit(ready_image, ready_image_rect)
        self.bg_surface.blit(inst_image, inst_image_rect)


class AdventureMenuScreen(Screen):
    """The "choose an adventure" screen."""

    def __init__(self, bg_surface, bg_color, mission_list):
        """Initialize screen attributes."""
        super().__init__(bg_surface, bg_color)
        self.mission_list = mission_list
        self.prep_objects()

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for title_msg in self.title_msgs:
                rect = pygame.Rect(
                        (title_msg['rect'].x + self.menu_surface_rect.x,
                            title_msg['rect'].y + self.menu_surface_rect.y),
                        (title_msg['rect'].width,
                            title_msg['rect'].height))
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.mission_list.set_active_mission(title_msg['mission'])
                    self.active = False

    def draw_objects(self):
        """Draw screen objects."""
        # Fill background color
        self.menu_surface.fill(self.bg_color)

        # Draw to menu_surface
        self.menu_surface.blit(self.heading_msg_image, (0,0))
        for title_msg in self.title_msgs:
            self.menu_surface.blit(title_msg['image'],
                    title_msg['rect'])

        # Draw menu to bg_surface
        self.bg_surface.blit(self.menu_surface, self.menu_surface_rect)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        heading_msg = "Choose an Adventure"

        # Render heading_msg
        self.heading_msg_image = self.title_font.render(heading_msg, True, self.text_color)
        heading_msg_image_rect = self.heading_msg_image.get_rect()

        # Grab bottom position of the heading for spacing next list entry
        last_msg_bottom = heading_msg_image_rect.bottom + 5

        # Render mission titles in list
        self.title_msgs = []
        for mission in self.mission_list.missions:
            title_msg = mission.title

            # Render title_msg and position centered below last line
            title_msg_image = self.basic_font.render(title_msg, True, self.text_color)
            title_msg_rect = title_msg_image.get_rect()
            title_msg_rect.centerx = heading_msg_image_rect.centerx
            title_msg_rect.top = last_msg_bottom + 5
            self.title_msgs.append(
                    {'mission': mission,
                        'image': title_msg_image, 'rect': title_msg_rect})

            last_msg_bottom = title_msg_rect.bottom

        # Create surface with width from heading and height from last msg.
        # This assumes that heading is always the longest string.
        self.menu_surface = pygame.Surface((heading_msg_image_rect.width,
                                 last_msg_bottom))
        self.menu_surface_rect = self.menu_surface.get_rect()
        self.menu_surface_rect.center = self.bg_surface_rect.center


class AdventureResultScreen(Screen):
    """The adventure result screen."""

    def __init__(self, bg_surface, bg_color, stats, avatar, mission):
        """Initialize screen attributes."""
        super().__init__(bg_surface, bg_color)
        self.stats = stats
        self.avatar = avatar
        self.mission = mission

        # Avatar and enemy start with full hp.
        self.avatar.heal()
        self.mission.enemy.heal()

        # Resolve combat result.
        self.mission.resolve_combat(avatar)
        self.stats.update(self.mission.result)

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        self.press_any_key(event)

    def draw_objects(self):
        """Draw screen objects."""
        self.draw_results()
        self.stats.draw(self.bg_surface)

    def draw_results(self):
        """Draw the results of the last combat."""

        if self.mission.result is None:
            result_msg = self.avatar.name + " withdrew."
        elif self.mission.result is True:
            result_msg = "Success! " + self.avatar.name + " won."
        else:
            result_msg = "Failure! " + self.avatar.name + " defeated."

        hp_msg = self.avatar.name + " HP: " + str(self.avatar.hp)

        # Render mission title and position slightly above center on bg_surface.
        title_msg_image = self.title_font.render(self.mission.title, True, self.text_color)
        title_msg_image_rect = title_msg_image.get_rect()
        title_msg_image_rect.centerx = self.bg_surface_rect.centerx
        title_msg_image_rect.bottom = self.bg_surface_rect.centery - 5

        # Render result_msg and position slightly below center on bg_surface.
        result_msg_image = self.basic_font.render(result_msg, True, self.text_color)
        result_msg_image_rect = result_msg_image.get_rect()
        result_msg_image_rect.centerx = self.bg_surface_rect.centerx
        result_msg_image_rect.top = self.bg_surface_rect.centery + 5

        # Render hp_msg and position below result_msg on bg_surface.
        hp_msg_image = self.basic_font.render(hp_msg, True, self.text_color)
        hp_msg_image_rect = hp_msg_image.get_rect()
        hp_msg_image_rect.centerx = self.bg_surface_rect.centerx
        hp_msg_image_rect.top = result_msg_image_rect.bottom + 5

        # Draw messages.
        self.bg_surface.blit(title_msg_image, title_msg_image_rect)
        self.bg_surface.blit(result_msg_image, result_msg_image_rect)
        self.bg_surface.blit(hp_msg_image, hp_msg_image_rect)

