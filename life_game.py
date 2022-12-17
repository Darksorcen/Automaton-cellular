import pygame
import sys
import utils

from grid import Grid
from conway_solver import ConwaySolver

pygame.init()


screen = pygame.display.set_mode((1080, 720))

SCREEN_SIZE = screen.get_size()
clock = pygame.time.Clock()
run = True

started = False
rsize = 10  # rect size
rsize_min = 8
rsize_max = 20

grid = Grid(SCREEN_SIZE, rsize)

# The grid is static, just draw it once
grid_surf = grid.get_surf(SCREEN_SIZE, rsize)

solver = ConwaySolver(SCREEN_SIZE, rsize)

lmb_pressed = False
rmb_pressed = False

finished = False

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

                grid.update(SCREEN_SIZE, rsize)
                grid_surf = grid.get_surf(SCREEN_SIZE, rsize)

            elif event.button == 5 and rsize > rsize_min:  # Mouse wheel down
                rsize -= 1

                grid.update(SCREEN_SIZE, rsize)
                grid_surf = grid.get_surf(SCREEN_SIZE, rsize)

        if event.type == pygame.MOUSEBUTTONUP and not started:
            if event.button == 1:
                lmb_pressed = False
            elif event.button == 3:
                rmb_pressed = False

    if lmb_pressed:
        pos = grid.get_mouse_pos_grid(rsize)
        solver.rects[pos] = True

    if rmb_pressed:
        pos = grid.get_mouse_pos_grid(rsize)
        solver.rects[pos] = False

    if started and not finished:
        pygame.time.wait(waiting_time)
        rects = solver.check_rules()

    screen.fill((0, 0, 0))

    screen.blit(grid_surf, (0, 0))

    grid.render(solver.rects, screen, (0, 255, 0))

    screen.blit(utils.debug_info(f"{clock.get_fps():.1f}"), (10, 10))

    pygame.display.flip()
    clock.tick(60)
