import pygame


class Grid:
    def __init__(self, screen_size: tuple[int, int], rsize: int):
        self.size = self.update_grid_size(screen_size, rsize)
        self.grid = self.generation(rsize)

    def generation(self, rsize: int) -> dict[tuple[int, int]: pygame.Rect]:
        """
        Generate a grid of rects
        """
        grid = {}
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                grid[(x, y)] = pygame.Rect(x*rsize,
                                           y*rsize,
                                           rsize,
                                           rsize)
        return grid

    def update_grid_size(self, size: tuple[int, int], rsize: int) \
            -> tuple[int, int]:
        return (size[0]//rsize, size[1]//rsize)

    def get_mouse_pos_grid(self, rsize: int) -> tuple[int, int]:
        """
        Convert mouse positions to grid pos [0, SCREEN_SIZE//rect_size]
        """
        mouse_pos = pygame.mouse.get_pos()
        pos = (mouse_pos[0]//rsize,
               mouse_pos[1]//rsize)
        return pos

    def get_surf(self,
                 size: tuple[int, int],
                 rsize: int) \
            -> pygame.Surface:
        """
        Create a surface containing the grid
        """
        surface = pygame.Surface(size)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                pygame.draw.line(surface,
                                 (90, 90,  90),
                                 [0, y*rsize],
                                 [self.size[0]*rsize, y*rsize])
            pygame.draw.line(surface,
                             (90, 90, 90),
                             [x*rsize, 0],
                             [x*rsize, self.size[1]*rsize])
        return surface

    def render(self, rects: dict[tuple[int, int]: bool],
               screen: pygame.Surface,
               rect_color: tuple[int, int, int]) -> None:
        """
        Render the grid onto the screen
        """
        for pos, rect in self.grid.items():
            if rects.get(pos, False):
                pygame.draw.rect(screen, rect_color, self.grid[pos])
