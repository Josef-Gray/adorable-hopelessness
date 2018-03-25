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
        self.alt_text_color = (100, 100, 100)
        self.title_font = pygame.font.SysFont(None, 42)
        self.basic_font = pygame.font.SysFont(None, 36)
        self.alt_font = pygame.font.SysFont(None, 32)

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

    def __init__(self, bg, player):
        """Initialize screen attributes."""
        super().__init__(bg)
        self.player = player
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
            # Return ends name input and creates player
            elif event.key == pygame.K_RETURN:
                self.player.name = self.name_input
                self.player.log_properties()
                self.active = False

    def draw_objects(self):
        """Draw screen objects."""
        # Draw name prompt.
        self.bg.surface.blit(
                self.name_prompt_image, self.name_prompt_rect)

        # Render name input and position right of center on bg.surface.
        name_input_image = self.basic_font.render(
                self.name_input, True, self.text_color)
        name_input_rect = name_input_image.get_rect()
        name_input_rect.left = self.bg_rect.centerx + 10
        name_input_rect.centery = self.bg_rect.centery

        # Draw name input.
        self.bg.surface.blit(name_input_image, name_input_rect)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        self.name_prompt = "Name your character:"

        # Render name prompt and position left of center on bg.surface.
        self.name_prompt_image = self.basic_font.render(self.name_prompt, True, self.text_color)
        self.name_prompt_rect = self.name_prompt_image.get_rect()
        self.name_prompt_rect.right = self.bg_rect.centerx - 10
        self.name_prompt_rect.centery = self.bg_rect.centery


class CharacterScreen(Screen):
    """The character management screen."""

    def __init__(self, bg, player):
        """Initialize screen attributes."""
        self.player = player
        super().__init__(bg)

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if self.inst_rect.collidepoint(mouse_position):
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False

    def draw_objects(self):
        """Draw the prompt for game readiness."""
        self.bg.surface.blit(self.name_image, self.name_rect)
        self.bg.surface.blit(self.hp_image, self.hp_rect)
        self.bg.surface.blit(self.damage_image, self.damage_rect)
        self.bg.surface.blit(self.inst_image, self.inst_rect)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        # Render player max HP at the center of the screen.
        self.hp_image = self.basic_font.render("HP: " +
                str(self.player.max_hp), True, self.text_color)
        self.hp_rect = self.hp_image.get_rect()
        self.hp_rect.center = self.bg_rect.center

        # Render player name above HP.
        self.name_image = self.title_font.render(self.player.name, True,
                self.text_color)
        self.name_rect = self.name_image.get_rect()
        self.name_rect.centerx = self.bg_rect.centerx
        self.name_rect.bottom = self.hp_rect.top - 5

        # Render player damage below HP.
        self.damage_image = self.basic_font.render("Damage: " +
                str(self.player.min_damage) + "-" +
                str(self.player.max_damage), True, self.text_color)
        self.damage_rect = self.damage_image.get_rect()
        self.damage_rect.centerx = self.bg_rect.centerx
        self.damage_rect.top = self.hp_rect.bottom + 5

        # Render instruction and position at the center bottom of
        # bg.surface.
        inst_msg = "Press ESCAPE to return"
        self.inst_image = self.alt_font.render(
                inst_msg, True, self.alt_text_color)
        self.inst_rect = self.inst_image.get_rect()
        self.inst_rect.centerx = self.bg_rect.centerx
        self.inst_rect.bottom = self.bg_rect.bottom - 10


class ReadyScreen(Screen):
    """The "ready to adventure" screen."""

    def __init__(self, bg, player):
        """Initialize screen attributes."""
        self.player = player
        super().__init__(bg)

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if self.char_rect.collidepoint(mouse_position):
                CharacterScreen(self.bg, self.player).run()
            elif self.inst_rect.collidepoint(mouse_position):
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.active = False

    def draw_objects(self):
        """Draw the prompt for game readiness."""
        self.bg.surface.blit(self.ready_image, self.ready_rect)
        self.bg.surface.blit(self.inst_image, self.inst_rect)
        self.bg.surface.blit(self.char_image, self.char_rect)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        # Render question and position in the center of bg.surface.
        ready_msg = "Are you ready to adventure?"
        self.ready_image = self.basic_font.render(
                ready_msg, True, self.text_color)
        self.ready_rect = self.ready_image.get_rect()
        self.ready_rect.center = self.bg_rect.center

        # Render instruction and position at the center bottom of
        # bg.surface.
        inst_msg = "Press SPACE to continue"
        self.inst_image = self.alt_font.render(
                inst_msg, True, self.alt_text_color)
        self.inst_rect = self.inst_image.get_rect()
        self.inst_rect.centerx = self.bg_rect.centerx
        self.inst_rect.bottom = self.bg_rect.bottom - 10

        # Render Character screen button
        char_msg = "Character"
        self.char_image = self.alt_font.render(
                char_msg, True, self.alt_text_color)
        self.char_rect = self.char_image.get_rect()
        self.char_rect.top = 10
        self.char_rect.right = self.bg_rect.right - 10


class AdventureMenuScreen(Screen):
    """The "choose an adventure" screen."""

    def __init__(self, bg, mission_list):
        """Initialize screen attributes."""
        self.mission_list = mission_list
        super().__init__(bg)

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            for title_msg in self.title_msgs:
                rect = pygame.Rect(
                        (title_msg['rect'].x + self.menu_surface_rect.x,
                            title_msg['rect'].y + self.menu_surface_rect.y),
                        (title_msg['rect'].width,
                            title_msg['rect'].height))
                if rect.collidepoint(mouse_position):
                    self.mission_list.set_active_mission(title_msg['mission'])
                    self.active = False

    def draw_objects(self):
        """Draw screen objects."""
        # Fill background color
        self.menu_surface.fill(self.bg.color)

        # Draw to menu_surface
        self.menu_surface.blit(self.heading_image, (0,0))
        for title_msg in self.title_msgs:
            self.menu_surface.blit(title_msg['image'],
                    title_msg['rect'])

        # Draw menu to bg.surface
        self.bg.surface.blit(self.menu_surface, self.menu_surface_rect)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        heading_msg = "Choose an Adventure"

        # Render heading_msg
        self.heading_image = self.title_font.render(
                heading_msg, True, self.text_color)
        heading_rect = self.heading_image.get_rect()

        # Grab bottom position of the heading for spacing next list entry
        last_msg_bottom = heading_rect.bottom + 5

        # Render mission titles in list
        self.title_msgs = []
        for mission in self.mission_list.missions:
            title_msg = mission.title

            # Render title_msg and position centered below last line
            title_image = self.basic_font.render(
                    title_msg, True, self.text_color)
            title_rect = title_image.get_rect()
            title_rect.centerx = heading_rect.centerx
            title_rect.top = last_msg_bottom + 5
            self.title_msgs.append(
                    {'mission': mission,
                        'image': title_image, 'rect': title_rect})

            last_msg_bottom = title_rect.bottom

        # Create surface with width from heading and height from last msg.
        # This assumes that heading is always the longest string.
        self.menu_surface = pygame.Surface((heading_rect.width,
                                 last_msg_bottom))
        self.menu_surface_rect = self.menu_surface.get_rect()
        self.menu_surface_rect.center = self.bg_rect.center


class AdventureResultScreen(Screen):
    """The adventure result screen."""

    def __init__(self, bg, stats, player, mission):
        """Initialize screen attributes."""
        self.stats = stats
        self.player = player
        self.mission = mission

        # Player and enemy start with full hp.
        self.player.heal()
        self.mission.enemy.heal()

        # Resolve combat result.
        self.mission.resolve_combat(player)
        self.stats.update(self.mission.result)

        super().__init__(bg)

    def catch_special_events(self, event):
        """Catch screen-specific events."""
        self.press_any_key(event)

    def draw_objects(self):
        """Draw screen objects."""
        self.bg.surface.blit(self.title_image, self.title_rect)
        self.bg.surface.blit(self.result_image, self.result_rect)
        self.bg.surface.blit(self.hp_image, self.hp_rect)

        self.stats.draw(self.bg)

    def prep_objects(self):
        """Prepare fixed objects for drawing to the screen."""
        if self.mission.result == mission.WIN:
            result_msg = "Success! " + self.player.name + " won."
        elif self.mission.result == mission.RETREAT:
            result_msg = self.player.name + " withdrew."
        else:
            result_msg = "Failure! " + self.player.name + " defeated."

        hp_msg = self.player.name + " HP: " + str(self.player.hp)

        # Render mission title and position slightly above center on bg.surface.
        self.title_image = self.title_font.render(
                self.mission.title, True, self.text_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.bg_rect.centerx
        self.title_rect.bottom = self.bg_rect.centery - 5

        # Render result_msg and position slightly below center on bg.surface.
        self.result_image = self.basic_font.render(
                result_msg, True, self.text_color)
        self.result_rect = self.result_image.get_rect()
        self.result_rect.centerx = self.bg_rect.centerx
        self.result_rect.top = self.bg_rect.centery + 5

        # Render hp_msg and position below result_msg on bg.surface.
        self.hp_image = self.basic_font.render(
                hp_msg, True, self.text_color)
        self.hp_rect = self.hp_image.get_rect()
        self.hp_rect.centerx = self.bg_rect.centerx
        self.hp_rect.top = self.result_rect.bottom + 5

