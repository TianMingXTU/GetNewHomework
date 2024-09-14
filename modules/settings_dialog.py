from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QDialogButtonBox
from PyQt5.QtGui import QFontDatabase

class SettingsDialog(QDialog):
    """设置对话框"""

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("设置")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        font_label = QLabel("字体类型:")
        self.font_combo = QComboBox()
        fonts = QFontDatabase().families()
        self.font_combo.addItems(fonts)
        self.font_combo.setCurrentText(self.config.font_family)

        size_label = QLabel("字体大小:")
        self.size_spin = QSpinBox()
        self.size_spin.setMinimum(8)
        self.size_spin.setMaximum(48)
        self.size_spin.setValue(self.config.font_size)

        spacing_label = QLabel("行间距:")
        self.spacing_spin = QSpinBox()
        self.spacing_spin.setMinimum(1)
        self.spacing_spin.setMaximum(5)
        self.spacing_spin.setValue(self.config.line_spacing)

        layout.addWidget(font_label)
        layout.addWidget(self.font_combo)
        layout.addWidget(size_label)
        layout.addWidget(self.size_spin)
        layout.addWidget(spacing_label)
        layout.addWidget(self.spacing_spin)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.apply_settings)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

    def apply_settings(self):
        self.config.font_family = self.font_combo.currentText()
        self.config.font_size = self.size_spin.value()
        self.config.line_spacing = self.spacing_spin.value()
        self.config.save_user_config()
        self.accept()
