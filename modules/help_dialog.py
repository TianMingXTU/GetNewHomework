from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton

class HelpDialog(QDialog):
    """帮助文档对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("帮助文档")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        help_text = """
        <h2>欢迎使用智考AI</h2>
        <p>智考AI应用旨在帮助您基于上传的资料生成高质量的考试题目，并对您的答案进行智能化反馈。此系统支持多种题型、多语言编程环境，并具有现代化的UI设计和便捷的操作体验。</p>

        <h3>开始前的准备工作：</h3>
        <p>在开始生成题目和答题之前，您需要首先设置模型并输入API密钥。选择合适的AI模型能提高生成题目的效率和准确性。具体步骤如下：</p>
        <ol>
            <li>打开工具栏中的“<b>模型设置</b>”。</li>
            <li>在弹出的模型设置窗口中，选择您需要使用的AI模型，并输入您的API密钥。以下为模型支持的选项：</li>
        </ol>

        <h3>支持的模型：</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>模型名称</th>
                <th>描述</th>
                <th>上下文长度</th>
                <th>最大输出长度</th>
            </tr>
            <tr>
                <td><b>GLM-4-Plus</b></td>
                <td>高智能旗舰: 性能全面提升，长文本和复杂任务能力显著增强</td>
                <td>128K</td>
                <td>4K</td>
            </tr>
            <tr>
                <td><b>GLM-4-0520</b></td>
                <td>高智能模型：适用于处理高度复杂和多样化的任务</td>
                <td>128K</td>
                <td>4K</td>
            </tr>
            <tr>
                <td><b>GLM-4-Long</b></td>
                <td>超长输入：专为处理超长文本和记忆型任务设计</td>
                <td>1M</td>
                <td>4K</td>
            </tr>
            <tr>
                <td><b>GLM-4-Flash</b></td>
                <td>免费调用：智谱AI首个免费API，零成本调用大模型</td>
                <td>128K</td>
                <td>4K</td>
            </tr>
        </table>

        <h3>使用步骤：</h3>
        <ol>
            <li><b>设置模型和API：</b>点击工具栏中的“模型设置”，选择模型并输入API密钥。</li>
            <li><b>上传资料或输入内容：</b>您可以上传任何文件类型作为资料，或手动输入您想要的文本内容。系统支持所有常见文件类型（如PDF、TXT、DOCX等）。</li>
            <li><b>选择生成参数：</b>您可以选择题目的数量、难度（简单、中等、复杂）、类型（简答题、选择题、判断题、填空题、编程题）以及题目的语言（中文、英文、其他）。</li>
            <li><b>生成题目：</b>点击“生成题目”按钮，系统会根据输入的资料自动生成对应题目。题目生成时间取决于资料的内容量和题目的数量。</li>
            <li><b>输入答案并提交：</b>在生成的题目界面，输入您的答案后，点击“提交答案”按钮，系统会对您的答案进行评分和反馈。</li>
            <li><b>编程题环境：</b>如果生成的是编程题，系统会弹出一个独立的编程窗口，提供代码编写、运行和输出的完整功能。编程环境支持多语言（Python、JavaScript、C++等），并且以黑客风格的暗色主题呈现。</li>
            <li><b>查看统计信息和设置：</b>通过工具栏的菜单，您可以查看答题统计、调整设置以及获取帮助。</li>
        </ol>

        <h3>编程题弹窗环境：</h3>
        <ul>
            <li>选择编程语言：支持Python、JavaScript、C++等，编程环境根据语言提供自动补全和语法高亮。</li>
            <li>黑客风格编辑器：编辑器背景为黑色，文本为亮色，支持自动缩进、行号显示、代码折叠和补全功能。</li>
            <li>运行代码：在编写代码后，点击“运行代码”按钮，系统会执行代码并在输出窗口中显示结果。</li>
        </ul>

        <h3>快捷键说明：</h3>
        <ul>
            <li><b>Ctrl+O</b>：上传资料文件。</li>
            <li><b>Ctrl+I</b>：输入内容。</li>
            <li><b>Ctrl+G</b>：生成题目。</li>
            <li><b>Ctrl+S</b>：提交答案。</li>
            <li><b>Ctrl+Left</b>：查看上一题。</li>
            <li><b>Ctrl+Right</b>：查看下一题。</li>
        </ul>

        <h3>常见问题：</h3>
        <ul>
            <li><b>上传文件支持哪些类型？</b> 支持常见的文本文件如TXT、PDF、DOCX等。</li>
            <li><b>如何切换编程语言？</b> 在编程弹窗中，您可以通过语言下拉框选择Python、JavaScript、C++等不同的编程语言。</li>
            <li><b>反馈是实时的吗？</b> 是的，提交答案后系统会自动对您的答案进行评分，并提供智能反馈。</li>
            <li><b>如何设置API密钥和模型？</b> 请通过工具栏中的“模型设置”选择模型并输入API密钥。</li>
        </ul>

        <p>如有任何问题或建议，欢迎通过“意见反馈”功能与我们联系。</p>
        """


        help_label = QLabel(help_text, self)
        help_label.setWordWrap(True)
        help_label.setOpenExternalLinks(True)

        layout.addWidget(help_label)

        close_button = QPushButton("关闭", self)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)
