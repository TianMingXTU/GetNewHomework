from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox

class FeedbackDialog(QDialog):
    """意见反馈对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("意见反馈")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        instruction_label = QLabel("请在下面输入您的意见和建议：", self)
        layout.addWidget(instruction_label)

        self.feedback_edit = QTextEdit(self)
        self.feedback_edit.setPlaceholderText("请输入您的反馈...")
        layout.addWidget(self.feedback_edit)

        submit_button = QPushButton("提交", self)
        submit_button.clicked.connect(self.submit_feedback)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def submit_feedback(self):
        feedback_text = self.feedback_edit.toPlainText().strip()
        if feedback_text:
            # 这里可以将反馈发送到服务器或保存到本地文件
            try:
                # 假设保存到本地文件 feedback.txt
                with open("feedback.txt", "a", encoding="utf-8") as f:
                    f.write(feedback_text + "\n")
                QMessageBox.information(self, "感谢您的反馈", "您的反馈已提交，非常感谢！")
                self.accept()
            except Exception as e:
                QMessageBox.warning(self, "提交失败", f"提交反馈时出现错误：{e}")
        else:
            QMessageBox.warning(self, "提示", "反馈内容不能为空！")
