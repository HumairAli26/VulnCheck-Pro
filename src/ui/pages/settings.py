"""
SecureAudit
Settings Page

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout

from src.config.colors import colors
from src.config.fonts import fonts
from src.config.user_config import load_config, save_config
from src.ui.pages.base_page import BasePage
from src.ui.widgets.action_button import ActionButton
from src.ui.widgets.section_header import SectionHeader


class SettingsPage(BasePage):
    """Preferences persisted to config/user_settings.json."""

    def __init__(self):
        super().__init__()
        self._config = load_config()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout.addWidget(
            SectionHeader("Settings", "Configure how SecureAudit behaves")
        )

        self.main_layout.addWidget(self._label("Export Folder"))
        export_row = QHBoxLayout()
        self.export_folder_input = QLineEdit(self._config.export_folder)
        self.export_folder_input.setStyleSheet(self._input_style())
        browse_btn = ActionButton("Browse")
        browse_btn.clicked.connect(self._browse_folder)
        export_row.addWidget(self.export_folder_input, 1)
        export_row.addWidget(browse_btn)
        self.main_layout.addLayout(export_row)

        self.notifications_checkbox = QCheckBox("Enable notifications")
        self.notifications_checkbox.setChecked(self._config.notifications_enabled)
        self.notifications_checkbox.setStyleSheet(f"color:{colors.TEXT};")
        self.main_layout.addWidget(self.notifications_checkbox)

        self.scheduled_checkbox = QCheckBox("Enable scheduled scans (coming soon)")
        self.scheduled_checkbox.setChecked(self._config.scheduled_scans_enabled)
        self.scheduled_checkbox.setEnabled(False)
        self.scheduled_checkbox.setStyleSheet(f"color:{colors.SUBTEXT};")
        self.main_layout.addWidget(self.scheduled_checkbox)

        save_btn = ActionButton("Save Settings")
        save_btn.clicked.connect(self._save)
        self.main_layout.addWidget(save_btn)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(
            f'color:{colors.SUCCESS}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addStretch()

    def _label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(
            f'color:{colors.SUBTEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )
        return label

    def _input_style(self) -> str:
        return f"""
            QLineEdit {{
                background-color: {colors.CARD};
                color: {colors.TEXT};
                border: 1px solid {colors.BORDER};
                border-radius: 6px;
                padding: 8px;
            }}
        """

    def _browse_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Export Folder")
        if folder:
            self.export_folder_input.setText(folder)

    def _save(self) -> None:
        self._config.export_folder = self.export_folder_input.text()
        self._config.notifications_enabled = self.notifications_checkbox.isChecked()
        save_config(self._config)
        self.status_label.setText("Settings saved.")
