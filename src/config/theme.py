from src.config.colors import colors
from src.config.fonts import fonts


class Theme:

    @staticmethod
    def application():

        return f"""
        QWidget {{
            background: {colors.BACKGROUND};
            color: {colors.TEXT};
            font-family: "{fonts.FAMILY}";
            font-size: {fonts.BODY}pt;
        }}

        QPushButton {{
            border:none;
            border-radius:8px;
            padding:10px;
        }}

        QPushButton:hover {{
            background:{colors.CARD};
        }}

        QStatusBar {{
            background:{colors.SIDEBAR};
        }}
        """