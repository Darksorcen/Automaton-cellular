import pygame
import sys

from src.debug_info import debug_info
from src.grid import Grid
from src.conway_solver import ConwaySolver
from src.serializer import Serializer
from src.deserializer import Deserializer

pygame.init()


class Simulation:
    def __init__(self):

        self.screen = pygame.display.set_mode((1080, 720))

        self.SCREEN_SIZE = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.running = True

        self.started = False
        self.rsize = 10  # rect size
        self.rsize_min = 8
        self.rsize_max = 20

        self.grid = Grid(self.SCREEN_SIZE, self.rsize)

        # The grid is static, just draw it once
        self.grid_surf = self.grid.get_surf(self.SCREEN_SIZE, self.rsize)

        self.solver = ConwaySolver(self.SCREEN_SIZE, self.rsize)

        self.lmb_pressed = False
        self.rmb_pressed = False

        self.finished = False

        self.waiting_time = 0

        self.serializer = Serializer()
        self.deserializer = Deserializer()

        self.deserializer.read_json("data/simulation.json")
        self.data = self.deserializer.deserialize()

    def after_process(self):
        self.serializer.convert_data(self.solver.rects)
        self.serializer.write_to_json("data/simulation.json")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.runnning = False
                    pygame.display.quit()

                if event.key == pygame.K_SPACE:
                    self.started = True

                if event.key == pygame.K_o:
                    self.solver.add_new_rects(self.data)

            if event.type == pygame.MOUSEBUTTONDOWN and not self.started:
                if event.button == 1:    # Left mouse button
                    self.lmb_pressed = True
                elif event.button == 3:  # Right mouse button
                    self.rmb_pressed = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and self.rsize < self.rsize_max:  # Mouse wheel up
                    self.rsize += 1

                    self.grid.update(self.SCREEN_SIZE, self.rsize)
                    self.grid_surf = self.grid.get_surf(self.SCREEN_SIZE, self.rsize)

                elif event.button == 5 and self.rsize > self.rsize_min:  # Mouse wheel down
                    self.rsize -= 1

                    self.grid.update(self.SCREEN_SIZE, self.rsize)
                    self.grid_surf = self.grid.get_surf(self.SCREEN_SIZE, self.rsize)

            if event.type == pygame.MOUSEBUTTONUP and not self.started:
                if event.button == 1:
                    self.lmb_pressed = False
                elif event.button == 3:
                    self.rmb_pressed = False

    def update(self):
        if self.lmb_pressed:
            pos = self.grid.get_mouse_pos_grid(self.rsize)
            self.solver.rects[pos] = True

        if self.rmb_pressed:
            pos = self.grid.get_mouse_pos_grid(self.rsize)
            self.solver.rects[pos] = False

        if self.started and not self.finished:
            pygame.time.wait(self.waiting_time)
            self.solver.check_rules()


    def render(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.grid_surf, (0, 0))

        self.grid.render(self.solver.rects, self.screen, (0, 255, 0))

        self.screen.blit(debug_info(f"{self.clock.get_fps():.1f}"), (10, 10))

        pygame.display.flip()

    def run(self):
        # FIXED: complexity is too high
        while self.running:
            self.handle_events()
            self.update()
            try:
                self.render()
            except pygame.error as e:
                if e.args == ('display Surface quit',):
                    break

            self.clock.tick(60)
