import pygame_gui
import pygame

from typing import Hashable

class FileDialog:
    """
    A simpler object that UIFileDialog
    """

    def __init__(self,
                 rect: pygame.Rect,
                 manager: pygame_gui.UIManager,
                 initial_file_path: str,
                 title: str):

        self.ui_file_dialog = pygame_gui.windows.UIFileDialog(
                                        rect=rect,
                                        manager=manager,
                                        initial_file_path=initial_file_path,
                                        window_title=title)

        self.title = title
        self.rect = self.ui_file_dialog.rect
        self.visible = self.ui_file_dialog.visible

    def update(self):
        self.rect = self.ui_file_dialog.rect
        self.visible = self.ui_file_dialog.visible

    def is_path_picked(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            if event.ui_element == self.ui_file_dialog:
                return True

        return False

    def closed(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.ui_file_dialog:
                return True

        return False

    def hide(self):
        self.ui_file_dialog.hide()
        return self

    def show(self):
        self.ui_file_dialog.show()
        return self

    def get_hitbox(self):
        if self.visible:
            return self.rect
        return pygame.Rect(0, 0, 0, 0)

    def update_hitbox(self, hitboxes: dict[Hashable: pygame.Rect]):
        hitboxes[self.title] = self.get_hitbox()
        return hitboxes
