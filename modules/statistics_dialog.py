from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

class StatisticsDialog(QDialog):
    """显示用户答题统计信息的对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("统计信息")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 假设我们有以下统计数据，可以根据需要从父类或其他地方获取
        total_questions = self.parent().total_attempts
        correct_answers = self.parent().correct_answers
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        font = QFont()
        font.setPointSize(12)

        total_label = QLabel(f"总共回答的问题数：{total_questions}")
        total_label.setFont(font)
        correct_label = QLabel(f"答对的问题数：{correct_answers}")
        correct_label.setFont(font)
        accuracy_label = QLabel(f"正确率：{accuracy:.2f}%")
        accuracy_label.setFont(font)

        layout.addWidget(total_label)
        layout.addWidget(correct_label)
        layout.addWidget(accuracy_label)

        self.setLayout(layout)
