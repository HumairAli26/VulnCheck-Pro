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
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {colors.BORDER};
            border-radius: 5px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {colors.SUBTEXT};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}

        QScrollBar:horizontal {{
            background: transparent;
            height: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: {colors.BORDER};
            border-radius: 5px;
            min-width: 30px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {colors.SUBTEXT};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        """