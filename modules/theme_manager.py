class ThemeManager:
    """主题管理器"""

    def __init__(self, config):
        self.config = config

    def get_available_themes(self):
        """获取可用的主题列表"""
        return ["浅色模式", "深色模式", "蓝色模式", "绿色模式", "红色模式", "紫色模式"]

    def get_style_sheet(self):
        """根据当前主题返回样式表"""
        theme = self.config.current_theme
        font_family = self.config.font_family
        font_size = self.config.font_size
        line_spacing = self.config.line_spacing

        base_style = (
            f"font-family: {font_family};"
            f"font-size: {font_size}px;"
            f"line-height: {line_spacing};"
        )

        if theme == "浅色模式":
            return (
                f"""
                QWidget {{
                    background-color: #F5F5F5;
                    color: #000000;
                    {base_style}
                }}
                QPushButton {{
                    background-color: #FFFFFF;
                    color: #000000;
                    border-radius: 8px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: #E0E0E0;
                }}
                QLabel, QProgressBar, QTextEdit {{
                    background-color: #FFFFFF;
                    color: #000000;
                    border-radius: 8px;
                }}
            """
            )
        elif theme == "深色模式":
            return (
                f"""
                QWidget {{
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                    {base_style}
                }}
                QPushButton {{
                    background-color: #333333;
                    color: #FFFFFF;
                    border-radius: 8px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: #444444;
                }}
                QLabel, QProgressBar, QTextEdit {{
                    background-color: #333333;
                    color: #FFFFFF;
                    border-radius: 8px;
                }}
            """
            )
        elif theme == "蓝色模式":
            return (
                f"""
                QWidget {{
                    background-color: #D0E7FF;
                    color: #004488;
                    {base_style}
                }}
                QPushButton {{
                    background-color: #5C9BD1;
                    color: #FFFFFF;
                    border-radius: 8px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: #357ABD;
                }}
                QLabel, QProgressBar, QTextEdit {{
                    background-color: #FFFFFF;
                    color: #004488;
                    border-radius: 8px;
                }}
            """
            )
        elif theme == "绿色模式":
            return (
                f"""
                QWidget {{
                    background-color: #DFF0D8;
                    color: #3C763D;
                    {base_style}
                }}
                QPushButton {{
                    background-color: #5CB85C;
                    color: #FFFFFF;
                    border-radius: 8px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: #4CAE4C;
                }}
                QLabel, QProgressBar, QTextEdit {{
                    background-color: #FFFFFF;
                    color: #3C763D;
                    border-radius: 8px;
                }}
            """
            )
        elif theme == "红色模式":
            return (
                f"""
                QWidget {{
                    background-color: #F2DEDE;
                    color: #A94442;
                    {base_style}
                }}
                QPushButton {{
                    background-color: #D9534F;
                    color: #FFFFFF;
                    border-radius: 8px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: #C9302C;
                }}
                QLabel, QProgressBar, QTextEdit {{
                    background-color: #FFFFFF;
                    color: #A94442;
                    border-radius: 8px;
                }}
            """
            )
        elif theme == "紫色模式":
            return (
                f"""
                QWidget {{
                    background-color: #E6E6FA;
                    color: #4B0082;
                    {base_style}
                }}
                QPushButton {{
                    background-color: #9370DB;
                    color: #FFFFFF;
                    border-radius: 8px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: #7B68EE;
                }}
                QLabel, QProgressBar, QTextEdit {{
                    background-color: #FFFFFF;
                    color: #4B0082;
                    border-radius: 8px;
                }}
            """
            )
        else:
            return ""
