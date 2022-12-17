import pygame

from src.simulation import Simulation

pygame.init()

simulation = Simulation()
simulation.run()
simulation.after_process()
