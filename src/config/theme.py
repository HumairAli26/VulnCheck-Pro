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

        QScrollBar:vertical {{
            background: transparent;
            width: 10px;
        }}

        QScrollBar::handle:vertical {{
            background: {colors.BORDER};
            border-radius: 5px;
            min-height: 30px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {colors.SUBTEXT};
        }}

        QScrollBar::add-line, QScrollBar::sub-line {{
            height: 0px;
        }}

        QFrame#InfoCard {{
            background-color: {colors.CARD};
            border: none;
            border-radius: 14px;
        }}
        
        QFrame#InfoCard:hover {{
            background-color: {colors.CARD_HOVER};
        }}
        """