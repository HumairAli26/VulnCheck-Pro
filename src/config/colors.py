from dataclasses import dataclass

@dataclass(frozen=True)
class Colors:
    BACKGROUND = "#111827"
    SIDEBAR = "#0F172A"
    CARD = "#1F2937"
    PRIMARY = "#2563EB"
    SUCCESS = "#22C55E"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    TEXT = "#FFFFFF"
    SUBTEXT = "#94A3B8"

colors = Colors()