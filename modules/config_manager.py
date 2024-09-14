import json
import os

# modules/config_manager.py

class ConfigManager:
    """配置管理器"""

    def __init__(self):
        self.config_file = "user_config.json"
        self.font_size = 18
        self.line_spacing = 2
        self.font_family = "Arial"
        self.current_theme = "浅色模式"
        self.language = "中文"
        self.difficulty = "中等"
        self.question_type = "简答题"
        self.file_content = ""
        self.api_key = ""
        self.model_name = "glm-4-plus"
        self.load_user_config()

    def load_user_config(self):
        """加载用户配置"""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                self.font_size = config.get("font_size", self.font_size)
                self.current_theme = config.get("theme", self.current_theme)
                self.language = config.get("language", self.language)
                self.difficulty = config.get("difficulty", self.difficulty)
                self.question_type = config.get("question_type", self.question_type)
                self.api_key = config.get("api_key", self.api_key)
                self.model_name = config.get("model_name", self.model_name)
        else:
            self.save_user_config()

    def save_user_config(self):
        """保存用户配置"""
        config = {
            "font_size": self.font_size,
            "theme": self.current_theme,
            "language": self.language,
            "difficulty": self.difficulty,
            "question_type": self.question_type,
            "api_key": self.api_key,
            "model_name": self.model_name,
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
