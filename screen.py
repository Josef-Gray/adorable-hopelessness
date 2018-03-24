"""Classes for modeling game screens."""

import sys
import pygame
import re
import mission

class Screen():
    """A representation of a game screen."""

    def __init__(self, bg):
        """Initialize screen attributes."""
        self.bg = bg
        self.bg_rect = self.bg.surface.get_rect()

        self.text_color = (0, 0, 0)
        self.title_font = pygame.font.SysFont(None, 42)
        self.basic_font = pygame.font.SysFont(None, 36)

        # Render fixed objects.
        self.prep_objects()

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
        self.bg.surface.fill(self.bg.color)

        # Draw objects.
        self.draw_objects()

        # Make the most recently drawn bg.surface visible.
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
        """Overridable function for drawing screen-specific objects."""
        pass

    def prep_objects(self):
        """Overridable function for rendering screen-specific objects."""
        pass


class PlayerNameScreen(Screen):
    """The player name input screen."""

    def __init__(self, bg, avatar):
        """Initialize screen attributes."""
        super().__init__(bg)
        self.avatar = avatar
        self.name_input = ''

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        if event.type == pygame.KEYDOWN:
            # If a "word" character, append to input
            if re.match(r'\w', event.unicode):
                self.name_input += event.unicode
            # Backspace deletes the last letter
            elif event.key == pygame.K_BACKSPACE:
                self.name_input = self.name_input[:-1]
            # Return ends name input and creates avatar
            elif event.key == pygame.K_RETURN:
                self.avatar.name = self.name_input
                self.avatar.log_properties()
                self.active = False

    def draw_objects(self):
        """Draw screen objects."""
        # Draw name prompt.
        self.bg.surface.blit(
                self.name_prompt_image, self.name_prompt_image_rect)

        # Render name input and position right of center on bg.surface.
        name_input_image = self.basic_font.render(
                self.name_input, True, self.text_color)
        name_input_image_rect = name_input_image.get_rect()
        name_input_image_rect.left = self.bg_rect.centerx + 10
        name_input_image_rect.centery = self.bg_rect.centery

        # Draw name input.
        self.bg.surface.blit(name_input_image, name_input_image_rect)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        self.name_prompt = "Name your character:"

        # Render name prompt and position left of center on bg.surface.
        self.name_prompt_image = self.basic_font.render(self.name_prompt, True, self.text_color)
        self.name_prompt_image_rect = self.name_prompt_image.get_rect()
        self.name_prompt_image_rect.right = self.bg_rect.centerx - 10
        self.name_prompt_image_rect.centery = self.bg_rect.centery


class ReadyScreen(Screen):
    """The "ready to adventure" screen."""

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        self.press_any_key(event)

    def draw_objects(self):
        """Draw the prompt for game readiness."""
        self.bg.surface.blit(self.ready_image, self.ready_image_rect)
        self.bg.surface.blit(self.inst_image, self.inst_image_rect)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        # Render question and position in the center of bg.surface.
        ready_msg = "Are you ready to adventure?"
        self.ready_image = self.basic_font.render(
                ready_msg, True, self.text_color)
        self.ready_image_rect = self.ready_image.get_rect()
        self.ready_image_rect.center = self.bg_rect.center

        # Render instruction and position at the center bottom of
        # bg.surface.
        inst_msg = "Press SPACE to continue"
        inst_text_color = (100, 100, 100)
        inst_font = pygame.font.SysFont(None, 32)
        self.inst_image = inst_font.render(inst_msg, True, inst_text_color)
        self.inst_image_rect = self.inst_image.get_rect()
        self.inst_image_rect.centerx = self.bg_rect.centerx
        self.inst_image_rect.bottom = self.bg_rect.bottom - 10


class AdventureMenuScreen(Screen):
    """The "choose an adventure" screen."""

    def __init__(self, bg, mission_list):
        """Initialize screen attributes."""
        self.mission_list = mission_list
        super().__init__(bg)

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
        self.menu_surface.fill(self.bg.color)

        # Draw to menu_surface
        self.menu_surface.blit(self.heading_msg_image, (0,0))
        for title_msg in self.title_msgs:
            self.menu_surface.blit(title_msg['image'],
                    title_msg['rect'])

        # Draw menu to bg.surface
        self.bg.surface.blit(self.menu_surface, self.menu_surface_rect)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        heading_msg = "Choose an Adventure"

        # Render heading_msg
        self.heading_msg_image = self.title_font.render(
                heading_msg, True, self.text_color)
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
        self.menu_surface_rect.center = self.bg_rect.center


class AdventureResultScreen(Screen):
    """The adventure result screen."""

    def __init__(self, bg, stats, avatar, mission):
        """Initialize screen attributes."""
        self.stats = stats
        self.avatar = avatar
        self.mission = mission

        # Avatar and enemy start with full hp.
        self.avatar.heal()
        self.mission.enemy.heal()

        # Resolve combat result.
        self.mission.resolve_combat(avatar)
        self.stats.update(self.mission.result)

        super().__init__(bg)

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        self.press_any_key(event)

    def draw_objects(self):
        """Draw screen objects."""
        self.bg.surface.blit(self.title_msg_image, self.title_msg_image_rect)
        self.bg.surface.blit(self.result_msg_image, self.result_msg_image_rect)
        self.bg.surface.blit(self.hp_msg_image, self.hp_msg_image_rect)

        self.stats.draw(self.bg)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        if self.mission.result == mission.WIN:
            result_msg = "Success! " + self.avatar.name + " won."
        elif self.mission.result == mission.RETREAT:
            result_msg = self.avatar.name + " withdrew."
        else:
            result_msg = "Failure! " + self.avatar.name + " defeated."

        hp_msg = self.avatar.name + " HP: " + str(self.avatar.hp)

        # Render mission title and position slightly above center on bg.surface.
        self.title_msg_image = self.title_font.render(
                self.mission.title, True, self.text_color)
        self.title_msg_image_rect = self.title_msg_image.get_rect()
        self.title_msg_image_rect.centerx = self.bg_rect.centerx
        self.title_msg_image_rect.bottom = self.bg_rect.centery - 5

        # Render result_msg and position slightly below center on bg.surface.
        self.result_msg_image = self.basic_font.render(
                result_msg, True, self.text_color)
        self.result_msg_image_rect = self.result_msg_image.get_rect()
        self.result_msg_image_rect.centerx = self.bg_rect.centerx
        self.result_msg_image_rect.top = self.bg_rect.centery + 5

        # Render hp_msg and position below result_msg on bg.surface.
        self.hp_msg_image = self.basic_font.render(
                hp_msg, True, self.text_color)
        self.hp_msg_image_rect = self.hp_msg_image.get_rect()
        self.hp_msg_image_rect.centerx = self.bg_rect.centerx
        self.hp_msg_image_rect.top = self.result_msg_image_rect.bottom + 5

