import pygame
import sys
import itertools
import utils
#from grid import get_mouse_pos_grid, update_grid_size, grid_generation, draw_grid  # FIXED:
from grid import Grid

pygame.init()


def check_rules(rects: dict[tuple[int, int]: bool],
                grid: Grid) \
                -> dict[tuple[int, int]: bool]:
    """
    Check the rules of Conway's Game of Life
    """
    # FIXME: to comment
    # FIXME: maybe change the way of affecting permutations
    # TOADD: customizing rules
    # (0, 1), (0, -1), (1, 0), (1, -1), (-1, 0), (-1, 1), (1, 1), (-1, -1)]
    permutations = list(itertools.permutations((0, 1, -1), 2))
    permutations += [(1, 1), (-1, -1)]

    new_dict = dict()
    for pos in grid.grid.keys():
        count = 0
        alive = False
        if rects.get(pos, False):
            alive = True

        # count all neighbors alive
        for i in range(len(permutations)):
            if count > 3:
                break
            pos_to_get = (pos[0]+permutations[i][0], pos[1]+permutations[i][1])
            count += rects.get(pos_to_get, 0)

        if (count == 2 or count == 3) and alive:
            new_dict[pos] = True
        elif count == 3 and not alive:
            new_dict[pos] = True
        else:
            new_dict[pos] = False
    return new_dict


#def create_surface(size: tuple[int, int],
#                   rects: list[pygame.Rect],
#                   color: tuple[int, int, int]) \
#                   -> pygame.Surface:
#    surf = pygame.Surface(size)
#    for rect in rects:
#        pygame.draw.rect(surf, color, rect)
#    return surf


screen = pygame.display.set_mode((1080, 720))

SCREEN_SIZE = screen.get_size()
clock = pygame.time.Clock()
run = True

started = False
rsize = 10  # rect size
rsize_min = 8
rsize_max = 20

grid = Grid(SCREEN_SIZE, rsize)
# Generate all rects in the grid
grid.generation(rsize)

# {(posx, posy): bool}
rects = dict()

lmb_pressed = False
rmb_pressed = False

finished = False

# The grid is static, just draw it once
grid_surf = grid.get_surf(screen.get_size(), rsize)

waiting_time = 0

# FIXME: complexity is too high
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
            if event.button == 4 and rsize < rsize_max:  # Mouse wheel up
                rsize += 1

                grid.size = grid.update_grid_size(screen.get_size(), rsize)
                grid.grid = grid.generation(rsize)  # FIXME: update grid
                grid_surf = grid.get_surf(screen.get_size(), rsize)
            elif event.button == 5 and rsize > rsize_min:  # Mouse wheel down
                rsize -= 1

                grid.size = grid.update_grid_size(screen.get_size(), rsize)
                grid.grid = grid.generation(rsize)
                grid_surf = grid.get_surf(screen.get_size(), rsize)
        if event.type == pygame.MOUSEBUTTONUP and not started:
            if event.button == 1:
                lmb_pressed = False
            elif event.button == 3:
                rmb_pressed = False

    if lmb_pressed:
        pos = grid.get_mouse_pos_grid(rsize)
        rects[pos] = True

    if rmb_pressed:
        # FIXME: abstraction of grid (mouse pos)
        pos = grid.get_mouse_pos_grid(rsize)
        rects[pos] = False

    if started and not finished:
        pygame.time.wait(waiting_time)
        temp_dict = rects.copy()
        rects = check_rules(rects, grid)

        # Create a surface when rects are static for optimizing performance
        #if temp_dict == rects:
        #    finished = True
        #    rects_list = []
        #    for pos, to_draw in rects.items():
        #        if to_draw:
        #            rects_list.append(grid.grid[pos]) # FIXME: grid.grid
        #    rects_surface = create_surface(screen.get_size(),
        #                                   rects_list,
        #                                   (0, 255, 0))
        #    rects_surface.set_colorkey((0, 0, 0))
        #    del temp_dict
        #    del rects_list

    screen.fill((0, 0, 0))

    screen.blit(grid_surf, (0, 0))

    grid.render(rects, screen, (0, 255, 0))

    screen.blit(utils.debug_info(f"{clock.get_fps():.1f}"), (10, 10))

    pygame.display.flip()
    clock.tick(60)
