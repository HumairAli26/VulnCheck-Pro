"""
SecureAudit
Remediation Steps Dialog
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
    QWidget
)

from src.config.colors import Colors, colors
from src.config.fonts import fonts
from src.models.audit_result import AuditResult
from src.services.remediation.remediation_guide import RemediationGuide, get_remediation


class RemediationDialog(QDialog):
    def __init__(self, result: AuditResult, parent=None):
        super().__init__(parent)
        self._result = result
        self._guide: RemediationGuide = get_remediation(result)
        self.setWindowTitle(f"How to fix: {result.title}")
        
        # Larger default size for complex remediation
        self.resize(700, 800)
        self.setStyleSheet(f"QDialog {{ background-color: {colors.BACKGROUND}; }}")
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(28, 24, 28, 24)
        outer.setSpacing(16)

        accent = Colors.for_severity(self._result.severity.value)

        # Header
        heading = QLabel(self._result.title)
        heading.setStyleSheet(f'color:{colors.TEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.HEADING}pt; font-weight:800;')
        outer.addWidget(heading)

        meta = QLabel(f"Severity: {self._result.severity.value}   ·   Estimated time: {self._guide.estimated_time}")
        meta.setStyleSheet(f'color:{accent}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt; font-weight:600;')
        outer.addWidget(meta)

        # Capped & Scrollable Threat Section
        if self._guide.threat:
            threat_box = QFrame()
            threat_box.setMaximumHeight(200) 
            threat_box.setStyleSheet(f"background-color: {accent}18; border: 1px solid {accent}55; border-radius: 10px;")
            
            t_layout = QVBoxLayout(threat_box)
            t_layout.setContentsMargins(16, 12, 16, 12)
            
            threat_title = QLabel("What could happen if this isn't fixed")
            threat_title.setStyleSheet(f'color:{accent}; font-weight:800;')
            t_layout.addWidget(threat_title)
            
            # Internal scroll area for long threat text
            threat_scroll = QScrollArea()
            threat_scroll.setWidgetResizable(True)
            threat_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
            
            threat_text = QLabel(self._guide.threat)
            threat_text.setWordWrap(True)
            threat_text.setStyleSheet("background: transparent; color: white;")
            
            threat_scroll.setWidget(threat_text)
            t_layout.addWidget(threat_scroll)
            outer.addWidget(threat_box)

        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background-color:{colors.BORDER};")
        outer.addWidget(divider)

        # Scrollable Steps Area
        steps_container = QWidget()
        steps_layout = QVBoxLayout(steps_container)
        steps_layout.setAlignment(Qt.AlignTop)

        for index, step in enumerate(self._guide.steps, start=1):
            steps_layout.addWidget(self._build_step_row(index, step, accent))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(steps_container)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Stretch factor 1 allows scroll area to fill all remaining vertical space
        outer.addWidget(scroll, 1)

        # Footer Buttons
        button_row = QHBoxLayout()
        button_row.addStretch()
        
        copy_btn = QPushButton("Copy Steps")
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setStyleSheet(self._button_style(colors.CARD, colors.TEXT))
        copy_btn.clicked.connect(self._copy_steps)
        button_row.addWidget(copy_btn)

        close_btn = QPushButton("Close")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(self._button_style(colors.PRIMARY, "#FFFFFF"))
        close_btn.clicked.connect(self.accept)
        button_row.addWidget(close_btn)

        outer.addLayout(button_row)

    def _build_step_row(self, index: int, text: str, accent: str) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        badge = QLabel(str(index))
        badge.setFixedSize(26, 26)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(f"background-color: {accent}33; color: {accent}; border-radius: 13px; font-weight: 700;")
        
        label = QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(badge)
        layout.addWidget(label)
        return row

    @staticmethod
    def _button_style(bg: str, fg: str) -> str:
        return f"QPushButton {{ background-color: {bg}; color: {fg}; border-radius: 8px; padding: 10px 18px; font-weight: 600; }}"

    def _copy_steps(self) -> None:
        text = "\n".join(f"{i}. {s}" for i, s in enumerate(self._guide.steps, start=1))
        QApplication.clipboard().setText(text)