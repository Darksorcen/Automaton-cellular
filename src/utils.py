import pygame


def debug_info(text: str,
               default_font: str = "arial",
               default_size: int = 30,
               default_color: tuple[int, int, int] = (255, 0, 0)) \
               -> pygame.Surface:
    if pygame.font.match_font(default_font) is not None:
        font = pygame.font.SysFont(default_font, default_size)
    else:
        default_sys_font = pygame.font.get_default_font()
        font = pygame.font.SysFont(default_sys_font, default_size)

    text_surf = font.render(text, False, default_color)
    return text_surf
