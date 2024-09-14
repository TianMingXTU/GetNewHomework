import logging
from PyQt5.QtCore import QThread, pyqtSlot
from zhipuai import ZhipuAI

from .worker_signals import WorkerSignals

class FeedbackThread(QThread):
    """获取反馈的线程类"""

    def __init__(self, config, question, answer, signals):
        super().__init__()
        self.config = config
        self.question = question
        self.answer = answer
        self.signals = signals
        self.client = ZhipuAI(api_key=self.config.api_key)

    @pyqtSlot()
    def run(self):
        try:
            logging.info(f"开始获取问题 {self.question} 的反馈...")

            prompt = (
                f"你是一名专业的教育评估专家，性格叛逆。请对以下{self.config.language}答案进行公正评分（0-100分），"
                "并说明评分理由，同时提供正确答案。"
                f"\n题目：{self.question}"
                f"\n学生的回答：{self.answer}"
            )

            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                stream=True,
            )

            for chunk in response:
                delta = chunk.choices[0].delta
                content = getattr(delta, "content", "")
                if content:
                    cleaned_content = self.clean_markdown(content)
                    self.signals.result.emit(cleaned_content)

        except Exception as e:
            logging.error(f"获取反馈时出错: {e}")
            self.signals.error.emit(f"获取反馈时出错: {e}")
        finally:
            self.signals.complete.emit()

    def clean_markdown(self, text):
        """移除Markdown格式的符号，返回纯文本"""
        return text.replace("*", "").replace("#", "")
