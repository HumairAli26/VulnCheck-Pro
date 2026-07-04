from dataclasses import dataclass

@dataclass(frozen=True)
class Fonts:
    FAMILY = "Segoe UI"
    TITLE = 24
    HEADING = 18
    BODY = 11
    SMALL = 10

fonts = Fonts()