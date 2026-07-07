from dataclasses import dataclass

@dataclass(frozen=True)
class Fonts:
    FAMILY = "Segoe UI"
    TITLE = 24
    HEADING = 18
    BODY = 15
    SMALL = 11

fonts = Fonts()