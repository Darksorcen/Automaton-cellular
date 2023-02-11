import itertools


class ConwaySolver:
    def __init__(self, screen_size: tuple[int, int], rsize: int):
        # {(posx, posy): bool}
        self.rects = dict()

        for x in range(screen_size[0]//rsize):
            for y in range(screen_size[1]//rsize):
                self.rects[(x, y)] = False

        self.permutations = list(itertools.permutations((0, 1, -1), 2))
        self.permutations += [(1, 1), (-1, -1)]

    def add_new_rects(self, to_add: dict[tuple[int, int]: bool]) -> None:
        """
        Superimpose the rectangles
        """
        for pos, v in to_add.items():
            if self.rects.get(pos, None) is not None:
                self.rects[pos] = v | self.rects[pos]

    # FIXME: regroup the two methods in two one
    def add_new_rectsl(self, to_add: list[tuple[int, int]]) -> None:
        """
        Superimpose the rectangles
        """
        for pos in to_add:
            if self.rects.get(pos, None) is not None:
                self.rects[pos] = 1 | self.rects[pos]

    def remove_rects(self, to_remove: list[tuple[int, int]]) -> None:
        """
        Remove the rectangles
        """
        for pos in to_remove:
            if self.rects.get(pos, None) is not None:
                self.rects[pos] = 0

    def check_rules(self) -> None:
        """
        Check the rules of Conway's Game of Life
        """
        # FIXME: to comment
        # FIXME: maybe change the way of affecting self.permutations
        # TOADD: customizing rules
        # (0, 1), (0, -1), (1, 0), (1, -1), (-1, 0), (-1, 1), (1, 1), (-1, -1)]

        new_rects = dict()
        for pos, val in self.rects.items():
            count = 0
            alive = val

            # count all neighbors alive
            for i in range(len(self.permutations)):
                if count > 3:
                    break
                pos_to_get = (pos[0]+self.permutations[i][0],
                              pos[1]+self.permutations[i][1])

                count += self.rects.get(pos_to_get, 0)

            if (count == 2 or count == 3) and alive:
                new_rects[pos] = True
            elif count == 3 and not alive:
                new_rects[pos] = True
            else:
                new_rects[pos] = False

        self.rects = new_rects
