from dataclasses import dataclass

@dataclass(frozen=True)
class Fonts:
    FAMILY = "Segoe UI"
    TITLE = 24
    HEADING = 18
    BODY = 14
    SMALL = 12

fonts = Fonts()