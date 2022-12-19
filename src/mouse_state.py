import pygame


class MouseState:
    """
    Basic class for mouse's states
    """

    def __init__(self, screen_size: tuple[int, int]):
        self.pos = (screen_size[0]//2, screen_size[1]//2)
        self.old_pos = self.pos
        self.relative_velocity = (0, 0)
        self.relatives = (0, 0)

    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.relative_velocity = (self.pos[0]-self.old_pos[0],
                                  self.pos[1]-self.old_pos[1])
        self.old_pos = self.pos

        self.relatives = (self.relatives[0]+self.relative_velocity[0],
                          self.relatives[1]+self.relative_velocity[1])
