"""Functions for running adventures and displaying intro and results."""

import sys
import pygame

def choose_adventure(bg_surface, bg_color, missions):
    text_color = (0, 0, 0)
    heading_font = pygame.font.SysFont(None, 42)
    title_font = pygame.font.SysFont(None, 36)

    heading_msg = "Choose an Adventure"
    
    # Render heading_msg
    heading_msg_image = heading_font.render(heading_msg, True, text_color)
    heading_msg_image_rect = heading_msg_image.get_rect()

    # Grab bottom position of the heading for spacing next list entry
    last_msg_bottom = heading_msg_image_rect.bottom + 5

    # Render mission titles in list
    title_msgs = []
    for mission in missions:
        title_msg = mission.title

        # Render title_msg and position centered below last line
        title_msg_image = title_font.render(title_msg, True, text_color)
        title_msg_rect = title_msg_image.get_rect()
        title_msg_rect.centerx = heading_msg_image_rect.centerx
        title_msg_rect.top = last_msg_bottom + 5
        title_msgs.append(
                {'mission': mission,
                    'image': title_msg_image, 'rect': title_msg_rect})

        last_msg_bottom = title_msg_rect.bottom

    # Create surface with width from heading and height from last msg.
    # This assumes that heading is always the longest string.
    surface = pygame.Surface((heading_msg_image_rect.width,
                             last_msg_bottom))
    surface_rect = surface.get_rect()
    bg_surface_rect = bg_surface.get_rect()
    surface_rect.center = bg_surface_rect.center

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for title_msg in title_msgs:
                    rect = pygame.Rect(
                            (title_msg['rect'].x + surface_rect.x,
                                title_msg['rect'].y + surface_rect.y),
                            (title_msg['rect'].width,
                                title_msg['rect'].height))
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        return title_msg['mission']

        bg_surface.fill(bg_color)
        # Have to use background color, not surface.set_alpha(0)
        # See https://github.com/renpy/pygame_sdl2/issues/24
        surface.fill(bg_color)

        # Draw text on surface
        surface.blit(heading_msg_image, (0,0))
        for title_msg in title_msgs:
            surface.blit(title_msg['image'], title_msg['rect'])

        # Draw surface to bg_surface
        bg_surface.blit(surface, surface_rect)

        pygame.display.flip()

