# modules/model_settings_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout

class ModelSettingsDialog(QDialog):
    """模型设置对话框"""

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("模型设置")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        api_key_label = QLabel("Zhipu AI API 密钥:")
        self.api_key_edit = QLineEdit(self)
        self.api_key_edit.setText(self.config.api_key)
        self.api_key_edit.setEchoMode(QLineEdit.Password)

        model_label = QLabel("选择模型:")
        self.model_combo = QComboBox(self)
        self.model_combo.addItems(["glm-4-flash", "glm-4-plus","glm-4-0520","glm-4-long"])
        self.model_combo.setCurrentText(self.config.model_name)

        layout.addWidget(api_key_label)
        layout.addWidget(self.api_key_edit)
        layout.addWidget(model_label)
        layout.addWidget(self.model_combo)

        button_layout = QHBoxLayout()
        save_button = QPushButton("保存", self)
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("取消", self)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_settings(self):
        self.config.api_key = self.api_key_edit.text().strip()
        self.config.model_name = self.model_combo.currentText()
        self.config.save_user_config()
        self.accept()
