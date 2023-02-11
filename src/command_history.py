import collections

from src.command import Command
from src.conway_solver import ConwaySolver


class CommandHistory:
    def __init__(self):
        self.commands = collections.deque()
        self.undoing = False

    def add(self, command: Command) -> None:
        self.commands.append(command)

    def undo(self, solver: ConwaySolver) -> None:
        try:
            last_command = self.commands[-1]

            match last_command.action:
                case "ADD":
                    solver.remove_rects(last_command.rects_pos)
                case "DEL":
                    # FIXME
                    print("HE")
                    solver.add_new_rectsl(last_command.rects_pos)
            self.commands.pop()
        except IndexError:
            pass
