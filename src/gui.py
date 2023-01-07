import pygame_gui
import pygame
import os


class GUI:
    def __init__(self, screen_size: tuple[int, int]):
        self.manager = pygame_gui.UIManager(screen_size, "assets/theme.json")
        self.hitboxes = []

        rel_rect = pygame.Rect((5, 5), (80, 35))
        self.hitboxes.append(rel_rect)
        self.debug_info = pygame_gui.elements.UILabel(relative_rect=rel_rect,
                                                      text="60",
                                                      manager=self.manager)

        rel_rect = pygame.Rect((100, 0), (60, 30))
        self.hitboxes.append(rel_rect)
        self.save_button = pygame_gui.elements.UIButton(relative_rect=rel_rect,
                                                        text="Save",
                                                        manager=self.manager)

        rel_rect = pygame.Rect((500, 100), (260, 300))
        self.hitboxes.append(rel_rect)
        path = os.getcwd()+"/assets/data"
        self.file_dialog = pygame_gui.windows.UIFileDialog(
                                                rect=rel_rect,
                                                manager=self.manager,
                                                initial_file_path=path)
        self.save_path = ""

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.save_button:
                self.file_dialog.visible = True

        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            if event.ui_element == self.file_dialog:
                self.save_path = event.text

        self.manager.process_events(event)

    def update(self, dt: float):
        if dt != 0:
            self.debug_info.set_text(f"{1/dt:.1f}")

        self.hitboxes[2] = self.file_dialog.rect
        self.manager.update(dt)

    def draw_ui(self, screen: pygame.Surface):
        self.manager.draw_ui(screen)
