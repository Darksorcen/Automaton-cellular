import pygame

pygame.init()


# FIXME: the fps are too low (5fps)
def check_rules(rects: dict[tuple[int, int]: pygame.Rect], grid):
    """
    Check the rules of Conway's Game of Life
    """
    new_dict = dict()
    for k, v in grid.items():
        count = 0
        alive = False
        if k in rects.keys():
            alive = True

        if rects.get((k[0]-1, k[1]-1)):
            count += 1
        if rects.get((k[0]-1, k[1])):
            count += 1
        if rects.get((k[0]+1, k[1])):
            count += 1
        if rects.get((k[0], k[1]-1)):
            count += 1
        if rects.get((k[0], k[1]+1)):
            count += 1
        if rects.get((k[0]-1, k[1]+1)):
            count += 1
        if rects.get((k[0]+1, k[1]-1)):
            count += 1
        if rects.get((k[0]+1, k[1]+1)):
            count += 1
        if (count == 2 or count == 3) and alive:
            new_dict[k] = v
        elif count == 3 and not alive:
            new_dict[k] = v
    return new_dict


def grid_generation(rect_size: int,
                    grid_size: tuple[int, int]) \
                    -> dict[tuple[int, int]: pygame.Rect]:
    """
    Generate a grid of rects
    """
    grid = {}
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            grid[(x, y)] = pygame.Rect(x*rect_size,
                                       y*rect_size,
                                       rect_size,
                                       rect_size)
    return grid


def update_grid_size(size: tuple[int, int], rect_size: int) -> tuple[int, int]:
    return (size[0]//rect_size, size[1]//rect_size)


def get_mouse_pos_grid(rect_size: int) -> tuple[int, int]:
    mouse_pos = pygame.mouse.get_pos()
    pos = (round(mouse_pos[0]//rect_size)*rect_size,
           round(mouse_pos[1]//rect_size)*rect_size)
    return pos

# FIXME: it break completely cell's logic
def update_rect_size(rects: dict[tuple[int, int]: pygame.Rect],
                     old_rect_size: int, new_rect_size: int) \
                     -> dict[tuple[int, int]: pygame.Rect]:
    new_rects = dict()
    for pos, r in rects.items():
        temp_tuple = (pos[0]*old_rect_size//new_rect_size,
                      pos[1]*old_rect_size//new_rect_size)
        new_rects[temp_tuple] = pygame.Rect(r.x//old_rect_size*new_rect_size,
                                            r.y//old_rect_size*new_rect_size,
                                            new_rect_size,
                                            new_rect_size)
    return new_rects


def draw_grid(size: tuple[int, int],
              grid_size: tuple[int, int],
              rect_size: int) \
              -> pygame.Surface:
    surface = pygame.Surface(size)
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            pygame.draw.line(surface,
                             (90, 90,  90),
                             [0, y*rect_size],
                             [grid_size[0]*rect_size, y*rect_size])
        pygame.draw.line(surface,
                         (90, 90, 90),
                         [x*rect_size, 0],
                         [x*rect_size, grid_size[1]*rect_size])
    return surface


screen = pygame.display.set_mode((1080, 720))

clock = pygame.time.Clock()
run = True

started = False
rect_size = 10
grid_size = update_grid_size(screen.get_size(), rect_size)

# Generate all rects in the grid
grid = grid_generation(rect_size, grid_size)

rects = dict()
lmb_pressed = False
rmb_pressed = False

# The grid is static, just draw it once
grid_surf = draw_grid(screen.get_size(), grid_size, rect_size)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                started = True

        if event.type == pygame.MOUSEBUTTONDOWN and not started:
            if event.button == 1:    # Left mouse button
                lmb_pressed = True
            elif event.button == 3:  # Right mouse button
                rmb_pressed = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            # FIXME: wheeling up or down doesn't change the grid
            if event.button == 4:  # Mouse wheel up
                print(rects)
                rects = update_rect_size(rects, rect_size, rect_size+1)
                print(rects)
                rect_size += 1
                grid_size = update_grid_size(screen.get_size(), rect_size)
                grid = grid_generation(rect_size, grid_size)
            elif event.button == 5:  # Mouse wheel down
                rects = update_rect_size(rects, rect_size, rect_size-1)
                rect_size -= 1
                grid_size = update_grid_size(screen.get_size(), rect_size)
                grid = grid_generation(rect_size, grid_size)

        if event.type == pygame.MOUSEBUTTONUP and not started:
            if event.button == 1:
                lmb_pressed = False
            elif event.button == 3:
                rmb_pressed = False

    if lmb_pressed:
        pos = get_mouse_pos_grid(rect_size)
        print(pos)
        rects[(pos[0]//rect_size, pos[1]//rect_size)] = pygame.Rect(*pos,
                                                                    rect_size,
                                                                    rect_size)

    if rmb_pressed:
        pos = get_mouse_pos_grid(rect_size)
        rects.pop((pos[0]//rect_size, pos[1]//rect_size), "KeyNotFound")

    if started:
        pygame.time.wait(100)
        rects = check_rules(rects, grid)

    screen.fill((0, 0, 0))

    screen.blit(grid_surf, (0, 0))

    for rect in rects.values():
        print(rect)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(rect.x,
                                                          rect.y,
                                                          rect.size[0],
                                                          rect.size[1]))

    pygame.display.flip()
    clock.tick(60)
    print(clock.get_fps())
