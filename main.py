import sys
import subprocess
import logging
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLabel, QTextEdit, QProgressBar,
    QFileDialog, QComboBox, QSpinBox, QScrollArea, QMessageBox, QDialog, QDialogButtonBox,
    QVBoxLayout, QFrame, QHBoxLayout, QMenu, QAction, QToolBar, QStatusBar, QShortcut
)
from PyQt5.QtCore import Qt, QTimer, QMutex, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QIcon, QKeySequence
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerJavaScript, QsciLexerCSharp
from PyQt5.QtWidgets import QStyle

from modules.worker_signals import WorkerSignals
from modules.generate_question_task import GenerateQuestionTask
from modules.feedback_thread import FeedbackThread
from modules.config_manager import ConfigManager
from modules.theme_manager import ThemeManager
from modules.file_manager import FileManager
from modules.settings_dialog import SettingsDialog
from modules.statistics_dialog import StatisticsDialog
from modules.help_dialog import HelpDialog
from modules.feedback_dialog import FeedbackDialog
from modules.model_settings_dialog import ModelSettingsDialog

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    filename="exam_app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class CodeEditorDialog(QDialog):
    """弹出式代码编辑器，支持多语言编程和执行"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编程环境")
        self.setGeometry(200, 150, 900, 600)
        self.init_ui()

    def init_ui(self):
        """初始化编程弹窗界面"""
        layout = QVBoxLayout(self)

        # 语言选择下拉框
        lang_layout = QHBoxLayout()
        self.language_combo = QComboBox(self)
        self.language_combo.addItems(["Python", "JavaScript", "C#", "C++"])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        lang_label = QLabel("选择语言:")
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo)

        layout.addLayout(lang_layout)

        # 创建代码编辑器
        self.code_editor = QsciScintilla(self)
        self.code_editor.setFont(QFont("Consolas", 14))
        self.code_editor.setAutoIndent(True)
        self.code_editor.setIndentationGuides(True)
        self.code_editor.setIndentationsUseTabs(False)
        self.code_editor.setTabWidth(4)
        self.code_editor.setMarginWidth(0, 40)
        self.code_editor.setCaretLineVisible(True)
        self.code_editor.setCaretLineBackgroundColor(Qt.darkGray)
        self.code_editor.setMarginsBackgroundColor(Qt.black)
        self.code_editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)  # 代码折叠
        self.code_editor.setMarginLineNumbers(1, True)  # 行号显示
        self.code_editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.code_editor.setAutoCompletionThreshold(2)  # 自动补全

        layout.addWidget(self.code_editor)

        # 输出结果显示
        self.output_display = QTextEdit(self)
        self.output_display.setFont(QFont("Consolas", 12))
        self.output_display.setReadOnly(True)
        layout.addWidget(self.output_display)

        # 编译和运行按钮
        self.run_button = QPushButton("运行代码", self)
        self.run_button.clicked.connect(self.run_code)
        layout.addWidget(self.run_button)

        # 初始化为Python语言
        self.change_language()

    def change_language(self):
        """根据选择的语言更改语法高亮和补全"""
        lang = self.language_combo.currentText()
        if lang == "Python":
            lexer = QsciLexerPython(self)
        elif lang == "JavaScript":
            lexer = QsciLexerJavaScript(self)
        elif lang == "C#":
            lexer = QsciLexerCSharp(self)
        else:  # 默认C++支持
            from PyQt5.Qsci import QsciLexerCPP
            lexer = QsciLexerCPP(self)

        # 设置语法高亮配色
        lexer.setPaper(Qt.black)  # 背景黑色
        lexer.setColor(Qt.green, lexer.Default)  # 默认字体颜色绿色
        lexer.setColor(Qt.yellow, lexer.CommentLine)  # 注释颜色黄色
        lexer.setColor(Qt.blue, lexer.String)  # 字符串颜色蓝色

        self.code_editor.setLexer(lexer)

    def run_code(self):
        """根据选择的语言运行代码"""
        code = self.code_editor.text()
        language = self.language_combo.currentText()

        # 根据语言选择编译器或解释器
        if language == "Python":
            self.execute_command(["python", "-c", code])
        elif language == "JavaScript":
            self.execute_command(["node", "-e", code])
        elif language == "C#":
            temp_file = self.save_code_to_tempfile("Program.cs", code)
            self.execute_command(["csc", temp_file, "/out:Program.exe"], post_command=["Program.exe"])
        elif language == "C++":
            temp_file = self.save_code_to_tempfile("program.cpp", code)
            self.execute_command(["g++", temp_file, "-o", "program"], post_command=["./program"])

    def save_code_to_tempfile(self, filename, code):
        """将代码保存到临时文件"""
        with open(filename, "w") as file:
            file.write(code)
        return filename

    def execute_command(self, command, post_command=None):
        """执行命令并显示结果"""
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            output = result.stdout + result.stderr
            self.output_display.setPlainText(output)

            # 如果有后续命令（如编译后运行）
            if post_command:
                post_result = subprocess.run(post_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
                post_output = post_result.stdout + post_result.stderr
                self.output_display.append(post_output)
        except Exception as e:
            self.output_display.setPlainText(f"运行时出错: {str(e)}")


class ExamApp(QWidget):
    """考试应用主界面"""

    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.theme_manager = ThemeManager(self.config)
        self.file_manager = FileManager()
        self.init_ui()

        self.mutex = QMutex()
        self.questions = []
        self.answers = {}
        self.feedback = {}
        self.timestamps = {}
        self.current_question_index = 0
        self.file_question_history = []
        self.running_threads = []
        self.total_attempts = 0
        self.correct_answers = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_backup)
        self.timer.start(300000)  # 每5分钟自动备份一次

        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self.save_buffer_to_file)
        self.save_timer.start(5000)  # 每5秒检查一次是否有数据需要保存

        # 快捷键支持
        self.setup_shortcuts()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("智考AI")
        self.setGeometry(100, 100, 1200, 800)
        main_layout = QVBoxLayout(self)

        # 菜单和工具栏
        self.create_menu_and_toolbar()

        # 设置部分
        settings_layout = QHBoxLayout()
        self.theme_combo = QComboBox(self)
        self.theme_combo.addItems(self.theme_manager.get_available_themes())
        self.theme_combo.setCurrentText(self.config.current_theme)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.theme_combo.setToolTip("选择主题风格")

        self.language_combo = QComboBox(self)
        self.language_combo.addItems(["中文", "英文", "日语", "法语", "德语"])
        self.language_combo.setCurrentText(self.config.language)
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.language_combo.setToolTip("选择语言")

        self.difficulty_combo = QComboBox(self)
        self.difficulty_combo.addItems(["简单", "中等", "复杂"])
        self.difficulty_combo.setCurrentText(self.config.difficulty)
        self.difficulty_combo.currentIndexChanged.connect(self.change_difficulty)
        self.difficulty_combo.setToolTip("选择题目难度")

        self.question_type_combo = QComboBox(self)
        self.question_type_combo.addItems(["简答题", "选择题", "判断题", "填空题", "编程题"])
        self.question_type_combo.setCurrentText(self.config.question_type)
        self.question_type_combo.currentIndexChanged.connect(self.change_question_type)
        self.question_type_combo.setToolTip("选择题目类型")

        settings_layout.addWidget(QLabel("主题:"))
        settings_layout.addWidget(self.theme_combo)
        settings_layout.addWidget(QLabel("语言:"))
        settings_layout.addWidget(self.language_combo)
        settings_layout.addWidget(QLabel("难度:"))
        settings_layout.addWidget(self.difficulty_combo)
        settings_layout.addWidget(QLabel("题型:"))
        settings_layout.addWidget(self.question_type_combo)

        main_layout.addLayout(settings_layout)

        # 生成题目部分
        generate_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        self.upload_button = QPushButton("上传资料", self)
        self.upload_button.clicked.connect(self.upload_files)
        open_icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        self.upload_button.setIcon(open_icon)
        self.upload_button.setToolTip("上传资料文件")

        self.text_input_button = QPushButton("输入内容", self)
        self.text_input_button.clicked.connect(self.open_text_input_dialog)
        new_icon = self.style().standardIcon(QStyle.SP_FileIcon)
        self.text_input_button.setIcon(new_icon)
        self.text_input_button.setToolTip("手动输入资料内容")

        top_layout.addWidget(self.upload_button)
        top_layout.addWidget(self.text_input_button)

        self.spin_box = QSpinBox(self)
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(50)
        self.spin_box.setValue(5)
        self.spin_box.setToolTip("选择要生成的题目数量")
        top_layout.addWidget(QLabel("题目数量:"))
        top_layout.addWidget(self.spin_box)

        self.generate_button = QPushButton("生成题目", self)
        self.generate_button.clicked.connect(self.start_question_generation)
        self.generate_button.setEnabled(False)
        generate_icon = self.style().standardIcon(QStyle.SP_CommandLink)
        self.generate_button.setIcon(generate_icon)
        self.generate_button.setToolTip("开始生成题目")
        top_layout.addWidget(self.generate_button)

        generate_layout.addLayout(top_layout)

        self.progress_bar = QProgressBar(self)
        generate_layout.addWidget(self.progress_bar)

        main_layout.addLayout(generate_layout)

        # 答题和反馈区域布局
        content_layout = QGridLayout()

        left_frame = QFrame(self)
        self.left_layout = QVBoxLayout(left_frame)

        self.question_label = QLabel("题目将显示在这里", self)
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont(self.config.font_family, self.config.font_size))

        question_scroll_area = QScrollArea(self)
        question_scroll_area.setWidget(self.question_label)
        question_scroll_area.setWidgetResizable(True)
        question_scroll_area.setFixedHeight(200)

        self.answer_edit = QTextEdit(self)
        self.answer_edit.setFont(QFont(self.config.font_family, self.config.font_size))
        self.answer_edit.setPlaceholderText("请输入您的答案...")
        self.answer_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.answer_edit.customContextMenuRequested.connect(self.show_context_menu)
        self.answer_edit.textChanged.connect(self.provide_real_time_feedback)

        self.submit_button = QPushButton("提交答案", self)
        self.submit_button.setEnabled(False)
        apply_icon = self.style().standardIcon(QStyle.SP_DialogApplyButton)
        self.submit_button.setIcon(apply_icon)
        self.submit_button.clicked.connect(self.submit_answer)
        self.submit_button.setToolTip("提交您的答案并获取反馈")

        navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一题", self)
        self.prev_button.setEnabled(False)
        back_icon = self.style().standardIcon(QStyle.SP_ArrowBack)
        self.prev_button.setIcon(back_icon)
        self.prev_button.clicked.connect(self.go_to_previous_question)
        self.prev_button.setToolTip("查看上一题")

        self.next_button = QPushButton("下一题", self)
        self.next_button.setEnabled(False)
        forward_icon = self.style().standardIcon(QStyle.SP_ArrowForward)
        self.next_button.setIcon(forward_icon)
        self.next_button.clicked.connect(self.go_to_next_question)
        self.next_button.setToolTip("查看下一题")

        navigation_layout.addWidget(self.prev_button)
        navigation_layout.addWidget(self.next_button)

        self.left_layout.addWidget(question_scroll_area)
        self.left_layout.addWidget(self.answer_edit)
        self.left_layout.addWidget(self.submit_button)
        self.left_layout.addLayout(navigation_layout)

        right_frame = QFrame(self)
        right_layout = QVBoxLayout(right_frame)

        self.feedback_label = QLabel("反馈将显示在这里", self)
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setFont(QFont(self.config.font_family, self.config.font_size))

        scroll_area_feedback = QScrollArea(self)
        scroll_area_feedback.setWidget(self.feedback_label)
        scroll_area_feedback.setWidgetResizable(True)

        right_layout.addWidget(scroll_area_feedback)

        content_layout.addWidget(left_frame, 0, 0)
        content_layout.addWidget(right_frame, 0, 1)

        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)
        self.apply_theme()

        # 状态栏
        self.status_bar = QStatusBar()
        main_layout.addWidget(self.status_bar)

    def create_menu_and_toolbar(self):
        """创建菜单和工具栏"""
        self.toolbar = QToolBar("Main Toolbar", self)
        self.toolbar.setMovable(False)

        help_action = QAction(QIcon.fromTheme("help-contents"), "帮助", self)
        help_action.triggered.connect(self.show_help_dialog)
        self.toolbar.addAction(help_action)

        feedback_action = QAction(QIcon.fromTheme("mail-send"), "意见反馈", self)
        feedback_action.triggered.connect(self.open_feedback_dialog)
        self.toolbar.addAction(feedback_action)

        settings_action = QAction(QIcon.fromTheme("preferences-system"), "设置", self)
        settings_action.triggered.connect(self.open_settings_dialog)
        self.toolbar.addAction(settings_action)

        stats_action = QAction(QIcon.fromTheme("view-statistics"), "统计", self)
        stats_action.triggered.connect(self.show_statistics)
        self.toolbar.addAction(stats_action)

        model_settings_action = QAction(QIcon.fromTheme("preferences-system-network"), "模型设置", self)
        model_settings_action.triggered.connect(self.open_model_settings_dialog)
        self.toolbar.addAction(model_settings_action)

        self.layout().addWidget(self.toolbar)

    def setup_shortcuts(self):
        """设置快捷键"""
        QShortcut(QKeySequence("Ctrl+O"), self, self.upload_files)
        QShortcut(QKeySequence("Ctrl+I"), self, self.open_text_input_dialog)
        QShortcut(QKeySequence("Ctrl+G"), self, self.start_question_generation)
        QShortcut(QKeySequence("Ctrl+S"), self, self.submit_answer)
        QShortcut(QKeySequence("Ctrl+Left"), self, self.go_to_previous_question)
        QShortcut(QKeySequence("Ctrl+Right"), self, self.go_to_next_question)

    def change_theme(self):
        """更改主题"""
        selected_theme = self.theme_combo.currentText()
        self.config.current_theme = selected_theme
        self.apply_theme()
        logging.info(f"用户切换为{self.config.current_theme}主题。")
        self.config.save_user_config()

    def change_language(self):
        """处理语言选择的更改"""
        self.config.language = self.language_combo.currentText()
        logging.info(f"用户选择了{self.config.language}语言")

    def change_difficulty(self):
        """处理难度选择的更改"""
        self.config.difficulty = self.difficulty_combo.currentText()
        logging.info(f"用户选择了{self.config.difficulty}难度")

    def change_question_type(self):
        """处理题型选择的更改"""
        self.config.question_type = self.question_type_combo.currentText()
        logging.info(f"用户选择了{self.config.question_type}题型")

    def apply_theme(self):
        """根据选择的主题应用不同的样式"""
        style_sheet = self.theme_manager.get_style_sheet()
        self.setStyleSheet(style_sheet)

    def auto_backup(self):
        """自动备份数据"""
        try:
            self.file_manager.backup_data()
            self.status_bar.showMessage("自动备份成功", 5000)
            logging.info("自动备份成功")
        except Exception as e:
            logging.error(f"自动备份失败: {e}")
            self.status_bar.showMessage("自动备份失败", 5000)

    def save_buffer_to_file(self):
        """批量保存队列中的数据到文件"""
        self.mutex.lock()
        try:
            if not self.file_manager.save_buffer:
                return
            self.file_manager.save_to_file()
            self.file_manager.save_buffer.clear()
        except Exception as e:
            logging.error(f"保存数据时出错: {e}")
            self.status_bar.showMessage("保存数据时出错", 5000)
        finally:
            self.mutex.unlock()

    def show_instructions(self):
        """显示使用说明"""
        dialog = HelpDialog(self)
        dialog.exec_()

    def upload_files(self):
        """上传文件功能"""
        try:
            file_names, _ = QFileDialog.getOpenFileNames(
                self,
                "选择文件",
                "",
                "All Files (*)",
            )
            if file_names:
                file_content = self.file_manager.read_files(file_names)
                self.config.file_content = file_content
                self.generate_button.setEnabled(True)
                self.file_question_history = []
                QMessageBox.information(self, "上传成功", "文件上传成功！")
                logging.info(f"文件上传成功: {file_names}")
        except Exception as e:
            logging.error(f"文件上传失败: {e}")
            QMessageBox.warning(self, "上传失败", "文件上传失败，请检查文件格式和内容。")

    def open_text_input_dialog(self):
        """打开文本输入对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("输入资料内容")
        dialog_layout = QVBoxLayout(dialog)
        text_edit = QTextEdit(dialog)
        text_edit.setPlaceholderText("在此输入您的资料内容...")
        dialog_layout.addWidget(text_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(
            lambda: self.set_file_content_from_text(text_edit.toPlainText(), dialog)
        )
        button_box.rejected.connect(dialog.reject)
        dialog_layout.addWidget(button_box)
        dialog.exec_()

    def set_file_content_from_text(self, text, dialog):
        """设置输入的内容为资料内容"""
        if text.strip():
            self.config.file_content = text.strip()
            self.generate_button.setEnabled(True)
            self.file_question_history = []
            logging.info("资料内容输入成功。")
            dialog.close()
            QMessageBox.information(self, "输入成功", "资料内容输入成功！")

    def start_question_generation(self):
        """开始生成题目"""
        if not self.config.file_content:
            self.question_label.setText("请先上传资料文件或输入资料内容！")
            return

        self.questions = []
        num_questions = self.spin_box.value()
        self.progress_bar.setMaximum(num_questions)
        self.progress_bar.setValue(0)
        self.current_question_index = 0

        logging.info(f"开始生成 {num_questions} 道题目。")
        self.generate_button.setEnabled(False)  # 禁用按钮，防止重复点击

        for _ in range(num_questions):
            try:
                task = GenerateQuestionTask(
                    self.config,
                    self.file_question_history,
                    self.add_question,
                )
                task.signals.result.connect(self.add_question)
                task.signals.complete.connect(self.on_question_generation_complete)
                task.signals.error.connect(self.handle_task_error)
                task.start()
                self.running_threads.append(task)
            except Exception as e:
                logging.error(f"启动生成题目任务时出错: {e}")
                QMessageBox.warning(self, "错误", "启动生成题目任务时出错，请重试。")
                self.generate_button.setEnabled(True)

    def add_question(self, question):
        """添加生成的问题"""
        self.mutex.lock()
        try:
            self.questions.append(question)
            self.file_question_history.append(question)
            self.timestamps[len(self.questions) - 1] = {
                "question_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.progress_bar.setValue(len(self.questions))
        finally:
            self.mutex.unlock()

    def on_question_generation_complete(self):
        """题目生成完成后，自动进入答题模式"""
        if len(self.questions) == self.progress_bar.maximum():
            self.current_question_index = 0
            self.display_next_question()
            self.submit_button.setEnabled(True)
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
            self.generate_button.setEnabled(True)  # 重新启用按钮

        # 从运行线程列表中移除完成的线程
        sender = self.sender()
        if sender in self.running_threads:
            self.running_threads.remove(sender)

    def handle_task_error(self, error_message):
        """处理任务中的错误"""
        logging.error(f"任务错误: {error_message}")
        QMessageBox.warning(self, "错误", f"任务执行时出错：{error_message}")
        self.generate_button.setEnabled(True)

    def submit_answer(self):
        """提交当前题目的答案并请求反馈"""
        current_answer = self.current_editor.text() if self.config.question_type == "编程题" else self.current_editor.toPlainText()
        current_answer = current_answer.strip()
        if not current_answer:
            QMessageBox.warning(self, "提示", "请先输入答案！")
            return

        question = self.questions[self.current_question_index]
        self.feedback_label.setText("等待反馈中...")
        self.feedback_label.setVisible(True)

        signals = WorkerSignals()
        signals.result.connect(self.update_feedback_display)
        signals.complete.connect(self.on_feedback_thread_complete)
        signals.error.connect(self.handle_task_error)

        try:
            task = FeedbackThread(
                self.config, question, current_answer, signals
            )
            self.answers[self.current_question_index] = current_answer
            self.timestamps[self.current_question_index][
                "answer_time"
            ] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task.start()
            self.running_threads.append(task)
        except Exception as e:
            logging.error(f"启动反馈任务时出错: {e}")
            QMessageBox.warning(self, "错误", "启动反馈任务时出错，请重试。")

    def update_feedback_display(self, feedback_part):
        """更新反馈显示区域"""
        current_text = self.feedback_label.text()
        self.feedback_label.setText(current_text + feedback_part)
        self.feedback[self.current_question_index] = self.feedback_label.text()
        self.timestamps[self.current_question_index][
            "feedback_time"
        ] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 将数据添加到保存队列
        self.file_manager.add_to_save_buffer(
            self.questions[self.current_question_index],
            self.answers.get(self.current_question_index, "无答案"),
            self.feedback.get(self.current_question_index, "无反馈"),
            self.timestamps.get(self.current_question_index, {}).get("question_time", ""),
            self.timestamps.get(self.current_question_index, {}).get("answer_time", ""),
            self.timestamps.get(self.current_question_index, {}).get("feedback_time", ""),
        )

    def on_feedback_thread_complete(self):
        """反馈线程完成后，从运行线程列表中移除"""
        sender = self.sender()
        if sender in self.running_threads:
            self.running_threads.remove(sender)

    def display_next_question(self):
        """显示当前的题目"""
        # 检查题目类型，如果是编程题，替换编辑器
        if self.config.question_type == "编程题":
            self.use_code_editor()
        else:
            self.use_text_editor()
        question_text = self.questions[self.current_question_index]
        self.question_label.setText(
            f"题目 {self.current_question_index + 1}: {question_text}"
        )

        if self.current_question_index in self.answers:
            if self.config.question_type == "编程题":
                self.current_editor.setText(self.answers[self.current_question_index])
            else:
                self.current_editor.setPlainText(self.answers[self.current_question_index])
        else:
            self.current_editor.clear()

        if self.current_question_index in self.feedback:
            self.feedback_label.setText(self.feedback[self.current_question_index])
        else:
            self.feedback_label.setText("反馈将显示在这里")

    def go_to_previous_question(self):
        """切换到上一题"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.display_next_question()

    def go_to_next_question(self):
        """切换到下一题"""
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.display_next_question()

    def show_context_menu(self, position):
        """右键菜单，增加复制粘贴功能"""
        menu = QMenu(self)
        copy_action = menu.addAction("复制")
        paste_action = menu.addAction("粘贴")
        cut_action = menu.addAction("剪切")
        select_all_action = menu.addAction("全选")

        action = menu.exec_(self.answer_edit.viewport().mapToGlobal(position))

        if action == copy_action:
            self.answer_edit.copy()
        elif action == paste_action:
            self.answer_edit.paste()
        elif action == cut_action:
            self.answer_edit.cut()
        elif action == select_all_action:
            self.answer_edit.selectAll()

    def use_code_editor(self):
        """使用代码编辑器"""
        if not hasattr(self, 'code_editor'):
            self.code_editor = QsciScintilla(self)
            lexer = QsciLexerPython()
            self.code_editor.setLexer(lexer)
            self.code_editor.setFont(QFont(self.config.font_family, self.config.font_size))
            self.code_editor.setMarginsFont(QFont(self.config.font_family, self.config.font_size))
            self.code_editor.setAutoIndent(True)
            self.code_editor.setIndentationGuides(True)
            self.code_editor.setIndentationsUseTabs(False)
            self.code_editor.setTabWidth(4)
            self.code_editor.setMarginWidth(0, 40)
            self.code_editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
            self.code_editor.setCaretLineVisible(True)
            self.code_editor.setCaretLineBackgroundColor(Qt.lightGray)
            self.code_editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)  # 代码折叠
            self.code_editor.setMarginLineNumbers(1, True)  # 显示行号
            self.code_editor.setAutoCompletionThreshold(2)  # 自动补全
            self.code_editor.setAutoCompletionSource(QsciScintilla.AcsAll)

        self.left_layout.replaceWidget(self.answer_edit, self.code_editor)
        self.answer_edit.hide()
        self.code_editor.show()
        self.current_editor = self.code_editor

    def use_text_editor(self):
        """使用普通文本编辑器"""
        if hasattr(self, 'code_editor') and self.code_editor.isVisible():
            self.left_layout.replaceWidget(self.code_editor, self.answer_edit)
            self.code_editor.hide()
            self.answer_edit.show()
        self.current_editor = self.answer_edit

    def open_settings_dialog(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self.config, self)
        dialog.exec_()
        self.apply_theme()

    def show_statistics(self):
        """显示统计信息"""
        dialog = StatisticsDialog(self)
        dialog.exec_()

    def show_help_dialog(self):
        """显示帮助文档"""
        dialog = HelpDialog(self)
        dialog.exec_()

    def open_feedback_dialog(self):
        """打开意见反馈对话框"""
        dialog = FeedbackDialog(self)
        dialog.exec_()

    def open_model_settings_dialog(self):
        """打开模型设置对话框"""
        dialog = ModelSettingsDialog(self.config, self)
        dialog.exec_()

    def provide_real_time_feedback(self):
        """实时提供反馈（示例，简单地统计字数）"""
        if self.config.question_type == "编程题":
            content = self.code_editor.text()
        else:
            content = self.answer_edit.toPlainText()
        word_count = len(content)
        self.status_bar.showMessage(f"当前字数：{word_count}")

    def export_data(self):
        """导出数据到 Excel 文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出数据", "", "Excel Files (*.xlsx)"
        )
        if file_path:
            try:
                self.file_manager.export_to_file(file_path)
                QMessageBox.information(self, "导出成功", "数据已成功导出！")
            except Exception as e:
                logging.error(f"导出失败: {e}")
                QMessageBox.warning(self, "导出失败", "数据导出失败，请重试。")

    def closeEvent(self, event):
        """在窗口关闭时释放资源"""
        self.timer.stop()
        self.save_timer.stop()
        self.save_buffer_to_file()

        # 等待所有线程结束
        for thread in self.running_threads:
            thread.quit()
            thread.wait()

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ExamApp()
    ex.show()
    sys.exit(app.exec_())

