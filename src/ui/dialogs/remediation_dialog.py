"""
SecureAudit
Remediation Steps Dialog

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.config.colors import Colors, colors
from src.config.fonts import fonts
from src.models.audit_result import AuditResult
from src.services.remediation.remediation_guide import RemediationGuide, get_remediation


class RemediationDialog(QDialog):
    """Shows a numbered, copyable walkthrough for fixing a single finding."""

    def __init__(self, result: AuditResult, parent=None):
        super().__init__(parent)
        self._result = result
        self._guide: RemediationGuide = get_remediation(result)
        self.setWindowTitle(f"How to fix: {result.title}")
        self.resize(620, 620)
        self.setStyleSheet(f"QDialog {{ background-color: {colors.BACKGROUND}; }}")
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(28, 24, 28, 24)
        outer.setSpacing(16)

        accent = Colors.for_severity(self._result.severity.value)

        heading = QLabel(self._result.title)
        heading.setStyleSheet(
            f'color:{colors.TEXT}; font-family:"{fonts.FAMILY}"; '
            f"font-size:{fonts.HEADING}pt; font-weight:800;"
        )
        outer.addWidget(heading)

        meta = QLabel(
            f"Severity: {self._result.severity.value}   ·   "
            f"Estimated time: {self._guide.estimated_time}"
            + ("   ·   Restart required" if self._guide.requires_restart else "")
        )
        meta.setStyleSheet(
            f'color:{accent}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt; font-weight:600;'
        )
        outer.addWidget(meta)

        if self._guide.threat:
            threat_box = QFrame()
            threat_box.setStyleSheet(
                f"""
                QFrame {{
                    background-color: {accent}18;
                    border: 1px solid {accent}55;
                    border-radius: 10px;
                }}
                """
            )
            threat_layout = QVBoxLayout(threat_box)
            threat_layout.setContentsMargins(16, 12, 16, 12)
            threat_layout.setSpacing(6)

            threat_title = QLabel("What could happen if this isn't fixed")
            threat_title.setStyleSheet(
                f'color:{accent}; font-family:"{fonts.FAMILY}"; '
                f"font-size:{fonts.SMALL}pt; font-weight:800; letter-spacing:0.4px;"
            )
            threat_layout.addWidget(threat_title)

            threat_text = QLabel(self._guide.threat)
            threat_text.setWordWrap(True)
            threat_text.setStyleSheet(
                f'color:{colors.TEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
            )
            threat_layout.addWidget(threat_text)

            outer.addWidget(threat_box)

        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background-color:{colors.BORDER};")
        outer.addWidget(divider)

        steps_container = QWidget()
        steps_layout = QVBoxLayout(steps_container)
        steps_layout.setSpacing(12)

        for index, step in enumerate(self._guide.steps, start=1):
            steps_layout.addWidget(self._build_step_row(index, step, accent))
        steps_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(steps_container)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        outer.addWidget(scroll, 1)

        if self._guide.references:
            refs = QLabel("Reference: " + ", ".join(self._guide.references))
            refs.setWordWrap(True)
            refs.setOpenExternalLinks(True)
            refs.setStyleSheet(
                f'color:{colors.INFO}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
            )
            outer.addWidget(refs)

        button_row = QHBoxLayout()
        button_row.addStretch()

        copy_btn = QPushButton("Copy Steps")
        copy_btn.setCursor(QCursor(Qt.PointingHandCursor))
        copy_btn.setStyleSheet(self._button_style(colors.CARD, colors.TEXT))
        copy_btn.clicked.connect(self._copy_steps)
        button_row.addWidget(copy_btn)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(self._button_style(colors.PRIMARY, "#FFFFFF"))
        close_btn.clicked.connect(self.accept)
        button_row.addWidget(close_btn)

        outer.addLayout(button_row)

    def _build_step_row(self, index: int, text: str, accent: str) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        badge = QLabel(str(index))
        badge.setFixedSize(26, 26)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(
            f"""
            background-color: {accent}33;
            color: {accent};
            border-radius: 13px;
            font-weight: 700;
            """
        )

        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(
            f'color:{colors.TEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.BODY}pt;'
        )

        layout.addWidget(badge, 0)
        layout.addWidget(label, 1)
        return row

    @staticmethod
    def _button_style(bg: str, fg: str) -> str:
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: 600;
            }}
        """

    def _copy_steps(self) -> None:
        numbered = "\n".join(
            f"{i}. {step}" for i, step in enumerate(self._guide.steps, start=1)
        )
        threat_block = f"Risk if unresolved:\n{self._guide.threat}\n\n" if self._guide.threat else ""
        text = f"{self._result.title}\n\n{threat_block}Steps:\n{numbered}"
        QApplication.clipboard().setText(text)
