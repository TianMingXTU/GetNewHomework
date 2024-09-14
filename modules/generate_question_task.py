import logging
from PyQt5.QtCore import QThread, pyqtSlot
from zhipuai import ZhipuAI

from .worker_signals import WorkerSignals

class GenerateQuestionTask(QThread):
    """生成问题的线程类"""

    def __init__(self, config, question_history, callback):
        super().__init__()
        self.config = config
        self.question_history = question_history
        self.callback = callback
        self.signals = WorkerSignals()
        self.client = ZhipuAI(api_key=self.config.api_key)

    @pyqtSlot()
    def run(self):
        try:
            logging.info("开始生成题目...")
            difficulty_prompt = self.config.difficulty
            question_type_prompt = self.config.question_type
            lang_prompt = self.config.language

            prompt = (
                f"你是一名专业的出题教授，请根据以下内容生成一个{difficulty_prompt}的{lang_prompt}{question_type_prompt}，"
                "要求题目专业严谨，不要提供答案，不要已生成的题目考察的内容相似。"
                f"\n内容：{self.config.file_content}"
                f"\n已生成的题目：\n{self.question_history}"
            )

            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            question = response.choices[0].message.content.strip()
            logging.info(f"成功生成题目: {question}")
            self.signals.result.emit(question)
        except Exception as e:
            logging.error(f"生成题目时出错: {e}")
            self.signals.error.emit(f"生成题目时出错: {e}")
        finally:
            self.signals.complete.emit()
