import pygame

from src.mouse_state import MouseState
from src.grid import Grid
from src.conway_solver import ConwaySolver
from src.serializer import Serializer
from src.deserializer import Deserializer
from src.gui import GUI

pygame.init()


class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((1080, 720))

        self.SCREEN_SIZE = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.dt = 1/60  # in seconds
        self.running = True

        self.started = False
        self.finished = False
        self.rsize = 10  # rect size
        self.rsize_min = 8
        self.rsize_max = 20

        self.grid = Grid(self.SCREEN_SIZE, self.rsize)

        # The grid is static, we just draw it once
        self.grid_surf = self.grid.get_surf(self.SCREEN_SIZE, self.rsize)

        self.solver = ConwaySolver(self.SCREEN_SIZE, self.rsize)

        self.lmb_pressed = False
        self.rmb_pressed = False

        self.waiting_time = 0

        self.serializer = Serializer()
        self.deserializer = Deserializer()

        self.deserializer.read_json("assets/data/glider_gun.json")
        self.data = self.deserializer.deserialize()

        self.start_superimpose = False

        self.mouse = MouseState(self.SCREEN_SIZE)

        self.center = pygame.Rect(0, 0, *self.SCREEN_SIZE).center
        self.cross_image = pygame.image.load("assets/images/little_cross.png")
        self.cross_image_center = (5, 5)

        self.gui = GUI(self.SCREEN_SIZE)

    def after_process(self):
        self.serializer.convert_data(self.solver.rects, self.rsize)
        self.serializer.write_to_json("assets/data/simulation.json")

    def calculate_positions_relative_to_center(self):
        """
        A method for calculating the new positions with respect to
        the actual mouse position
        It will make look like the squares loaded follow the mouse
        """
        dict_copy = dict()
        for pos, v in self.data.items():
            new_pos = (pos[0]+(self.mouse.relatives[0] // self.rsize),
                       pos[1]+(self.mouse.relatives[1] // self.rsize))
            dict_copy[new_pos] = v

        return dict_copy

    def handle_events(self):
        # FIXME: cyclomatic complexity is too high
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.display.quit()

            self.gui.handle_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.runnning = False
                    pygame.display.quit()

                if event.key == pygame.K_SPACE:
                    self.started = True

                if event.key == pygame.K_o:
                    self.start_superimpose = True

            if event.type == pygame.MOUSEBUTTONDOWN and not self.started:
                if event.button == 1:    # Left mouse button
                    self.lmb_pressed = True
                elif event.button == 3:  # Right mouse button
                    self.rmb_pressed = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse wheel up
                if event.button == 4 and self.rsize < self.rsize_max:
                    self.rsize += 1

                    self.grid.update(self.SCREEN_SIZE, self.rsize)
                    self.grid_surf = self.grid.get_surf(self.SCREEN_SIZE,
                                                        self.rsize)

                # Mouse wheel down
                elif event.button == 5 and self.rsize > self.rsize_min:
                    self.rsize -= 1

                    self.grid.update(self.SCREEN_SIZE, self.rsize)
                    self.grid_surf = self.grid.get_surf(self.SCREEN_SIZE,
                                                        self.rsize)

            if event.type == pygame.MOUSEBUTTONUP and not self.started:
                if event.button == 1:
                    self.lmb_pressed = False
                elif event.button == 3:
                    self.rmb_pressed = False

    def update(self):
        self.dt = self.clock.get_time()/1000

        self.mouse.update()
        self.gui.update(self.dt)

        if self.lmb_pressed:
            pos = self.grid.get_mouse_pos_grid(self.rsize)
            for hb in self.gui.hitboxes:
                if hb.collidepoint(self.mouse.pos):
                    break
            else:
                self.solver.rects[pos] = True

        if self.rmb_pressed:
            pos = self.grid.get_mouse_pos_grid(self.rsize)
            self.solver.rects[pos] = False

        if self.started and not self.finished:
            pygame.time.wait(self.waiting_time)
            self.solver.check_rules()

        # FIXME: continue, comment and refactor
        if self.start_superimpose:
            pos = self.grid.get_mouse_pos_grid(self.rsize)
            dict_copy = self.calculate_positions_relative_to_center()
            self.solver.add_new_rects(dict_copy)
            self.start_superimpose = False

        if self.gui.save_path != "":
            self.serializer.convert_data(self.solver.rects, self.rsize)
            self.serializer.write_to_json(self.gui.save_path)

    def render(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.grid_surf, (0, 0))

        self.grid.render(self.solver.rects, self.screen, (0, 255, 0))

        self.screen.blit(self.cross_image, (self.center[0]
                                            - self.cross_image_center[0],
                                            self.center[1]
                                            - self.cross_image_center[1]))

        self.gui.draw_ui(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            try:
                self.handle_events()
                self.update()
                self.render()
            except pygame.error as e:
                if e.args in (('display Surface quit',),
                              ('video system not initialized',)):
                    break
                else:
                    print(e.args)

            self.clock.tick(60)
