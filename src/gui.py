import pygame_gui
import pygame
import os

from src.file_dialog import FileDialog


class GUI:
    def __init__(self, screen_size: tuple[int, int]):
        self.manager = pygame_gui.UIManager(screen_size, "assets/theme.json")
        self.hitboxes = dict()

        tmp_rect = pygame.Rect((5, 5), (80, 35))
        self.hitboxes[1] = tmp_rect
        self.debug_info = pygame_gui.elements.UILabel(relative_rect=tmp_rect,
                                                      text="60",
                                                      manager=self.manager)

        offset = 1
        tmp_rect = pygame.Rect((100 - offset, 0 - offset), (80, 50))
        self.hitboxes[2] = tmp_rect
        self.save_button = pygame_gui.elements.UIButton(relative_rect=tmp_rect,
                                                        text="Save",
                                                        manager=self.manager)

        self.save_file_dialog = self.create_file_dialog("Path to save")

        # Visibility doesn't work so we move it out of the screen
        self.save_path = ""

        tmp_rect = pygame.Rect((200 - offset, 0 - offset), (80, 50))
        self.hitboxes[3] = tmp_rect
        self.load_button = pygame_gui.elements.UIButton(relative_rect=tmp_rect,
                                                        text="Load",
                                                        manager=self.manager)

        self.load_file_dialog = self.create_file_dialog("Path to load")

        self.load_path = ""

    def create_file_dialog(self, title: str):
        tmp_rect = pygame.Rect((500, 100), (260, 300))
        self.hitboxes[title] = tmp_rect

        initial_path = os.getcwd()+"/assets/data"
        return FileDialog(tmp_rect, self.manager, initial_path, title).hide()

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.save_button:
                self.save_file_dialog.show()

            elif event.ui_element == self.load_button:
                self.load_file_dialog.show()

        if self.save_file_dialog.is_path_picked(event):
            self.save_path = event.text
        elif self.load_file_dialog.is_path_picked(event):
            self.load_path = event.text

        if self.save_file_dialog.closed(event):

            print("Window closed")
            self.save_file_dialog = self.create_file_dialog("Path to save")

        if self.load_file_dialog.closed(event):
            self.load_file_dialog = self.create_file_dialog("Path to load")


            #initial_path = os.getcwd()+"/assets/data"
            #tmp_rect = pygame.Rect((-500, -500), (260, 300))
            #self.hitboxes.append(tmp_rect)
            #self.load_file_dialog = pygame_gui.windows.UIFileDialog(
            #                                        rect=tmp_rect,
            #                                        manager=self.manager,
            #                                        initial_file_path=initial_path,
            #                                        window_title="Path to load")

        self.manager.process_events(event)

    def update(self, dt: float):
        if dt != 0:
            self.debug_info.set_text(f"{1/dt:.1f}")

        self.save_file_dialog.update()
        self.load_file_dialog.update()

        # Check the hitboxes
        self.hitboxes = self.save_file_dialog.update_hitbox(self.hitboxes)
        self.hitboxes = self.load_file_dialog.update_hitbox(self.hitboxes)

        self.manager.update(dt)

    def draw_ui(self, screen: pygame.Surface):
        self.manager.draw_ui(screen)
