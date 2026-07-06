from dataclasses import dataclass

@dataclass(frozen=True)
class Colors:
    BACKGROUND = "#111827"
    SIDEBAR = "#0F172A"
    CARD = "#1F2937"
    CARD_HOVER = "#26313F"
    BORDER = "#2D3748"
    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"
    INFO = "#3B82F6"
    SUCCESS = "#22C55E"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    CRITICAL = "#991B1B"
    TEXT = "#FFFFFF"
    SUBTEXT = "#94A3B8"

    @staticmethod
    def for_severity(severity: str) -> str:
        """Maps a Severity enum value (e.g. 'High') to its accent color."""
        return {
            "Informational": Colors.INFO,
            "Low": Colors.SUCCESS,
            "Medium": Colors.WARNING,
            "High": Colors.DANGER,
            "Critical": Colors.CRITICAL,
        }.get(severity, Colors.SUBTEXT)

colors = Colors()