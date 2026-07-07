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
    DANGER = "#F62B2B"
    CRITICAL = "#860000"
    TEXT = "#FFFFFF"
    SUBTEXT = "#94A3B8"

    @staticmethod
    def for_severity(severity: str) -> str:
        mapping = {
            "Informational": Colors.INFO,
            "Low": Colors.SUCCESS,
            "Medium": Colors.WARNING,
            "High": Colors.DANGER,
            "Critical": Colors.CRITICAL,
        }
        return mapping.get(severity, Colors.SUBTEXT)

    @staticmethod
    def get_badge_style(severity: str) -> str:
        """Generates a soft-tinted stylesheet for severity badges."""
        color = Colors.for_severity(severity)
        # We use a semi-transparent background (10% opacity)
        return f"""
            QLabel {{
                color: {color};
                background-color: {color}20;
                border: 1px solid {color};
                border-radius: 4px;
                padding: 2px 8px;
                font-weight: bold;
            }}
        """

colors = Colors()