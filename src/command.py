class Command:
    def __init__(self, action: str, rects_pos: list[tuple[int, int]] = []):
        self.action = action
        self.rects_pos = rects_pos
