import pygame
import sys
import itertools
import utils

pygame.init()


def check_rules(rects: dict[tuple[int, int]: bool],
                grid: dict[tuple[int, int], pygame.Rect]) \
                -> dict[tuple[int, int]: bool]:
    """
    Check the rules of Conway's Game of Life
    """
    permutations = list(itertools.permutations((0, 1, -1), 2))
    permutations += [(1, 1), (-1, -1)]

    new_dict = dict()
    for k, v in grid.items():
        count = 0
        alive = False
        if rects.get(k, False):
            alive = True
        for i in range(len(permutations)):
            if count > 3:
                break
            pos_to_get = (k[0]+permutations[i][0], k[1]+permutations[i][1])
            count += rects.get(pos_to_get, 0)

        if (count == 2 or count == 3) and alive:
            new_dict[k] = True
        elif count == 3 and not alive:
            new_dict[k] = True
        else:
            new_dict[k] = False
    return new_dict


def grid_generation(rsize: int,
                    grid_size: tuple[int, int]) \
                    -> dict[tuple[int, int]: pygame.Rect]:
    """
    Generate a grid of rects
    """
    grid = {}
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            grid[(x, y)] = pygame.Rect(x*rsize,
                                       y*rsize,
                                       rsize,
                                       rsize)
    return grid


def update_grid_size(size: tuple[int, int], rsize: int) -> tuple[int, int]:
    return (size[0]//rsize, size[1]//rsize)


def get_mouse_pos_grid(rsize: int) -> tuple[int, int]:
    """
    Convert mouse positions to grid pos [0, SCREEN_SIZE//rect_size]
    """
    mouse_pos = pygame.mouse.get_pos()
    pos = (mouse_pos[0]//rsize,
           mouse_pos[1]//rsize)
    return pos


def draw_grid(size: tuple[int, int],
              grid_size: tuple[int, int],
              rsize: int) \
              -> pygame.Surface:
    surface = pygame.Surface(size)
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            pygame.draw.line(surface,
                             (90, 90,  90),
                             [0, y*rsize],
                             [grid_size[0]*rsize, y*rsize])
        pygame.draw.line(surface,
                         (90, 90, 90),
                         [x*rsize, 0],
                         [x*rsize, grid_size[1]*rsize])
    return surface


def create_surface(size: tuple[int, int],
                   rects: list[pygame.Rect],
                   color: tuple[int, int, int]) \
                   -> pygame.Surface:
    surf = pygame.Surface(size)
    for rect in rects:
        pygame.draw.rect(surf, color, rect)
    return surf


screen = pygame.display.set_mode((1080, 720))

clock = pygame.time.Clock()
run = True

started = False
rsize = 10  # rect size
rsize_min = 8
rsize_max = 20

grid_size = update_grid_size(screen.get_size(), rsize)

# Generate all rects in the grid
grid = grid_generation(rsize, grid_size)

# {(posx, posy): bool}
rects = dict()

lmb_pressed = False
rmb_pressed = False

finished = False

# The grid is static, just draw it once
grid_surf = draw_grid(screen.get_size(), grid_size, rsize)

waiting_time = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                sys.exit()
            if event.key == pygame.K_SPACE:
                started = True

        if event.type == pygame.MOUSEBUTTONDOWN and not started:
            if event.button == 1:    # Left mouse button
                lmb_pressed = True
            elif event.button == 3:  # Right mouse button
                rmb_pressed = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            # FIXED: wheeling up or down doesn't change the grid
            if event.button == 4 and rsize < rsize_max:  # Mouse wheel up
                rsize += 1

                grid_size = update_grid_size(screen.get_size(), rsize)
                grid = grid_generation(rsize, grid_size)
                grid_surf = draw_grid(screen.get_size(), grid_size, rsize)
            elif event.button == 5 and rsize > rsize_min:  # Mouse wheel down
                rsize -= 1

                grid_size = update_grid_size(screen.get_size(), rsize)
                grid = grid_generation(rsize, grid_size)
                grid_surf = draw_grid(screen.get_size(), grid_size, rsize)
        if event.type == pygame.MOUSEBUTTONUP and not started:
            if event.button == 1:
                lmb_pressed = False
            elif event.button == 3:
                rmb_pressed = False

    if lmb_pressed:
        pos = get_mouse_pos_grid(rsize)
        rects[pos] = True

    if rmb_pressed:
        pos = get_mouse_pos_grid(rsize)
        rects[pos] = False

    if started and not finished:
        pygame.time.wait(waiting_time)
        temp_dict = rects.copy()
        rects = check_rules(rects, grid)

        # Create a surface when rects are static for optimizing performance
        if temp_dict == rects:
            finished = True
            rects_list = []
            for pos, to_draw in rects.items():
                if to_draw:
                    rects_list.append(grid[pos])
            rects_surface = create_surface(screen.get_size(),
                                           rects_list,
                                           (0, 255, 0))
            rects_surface.set_colorkey((0, 0, 0))
            del temp_dict
            del rects_list

    screen.fill((0, 0, 0))

    screen.blit(grid_surf, (0, 0))

    if not finished:
        for pos, rect in grid.items():
            if rects.get(pos, False):
                pygame.draw.rect(screen, (0, 255, 0), grid[pos])
    else:
        screen.blit(rects_surface, (0, 0))

    screen.blit(utils.debug_info(f"{clock.get_fps():.1f}"), (10, 10))

    pygame.display.flip()
    clock.tick(60)
