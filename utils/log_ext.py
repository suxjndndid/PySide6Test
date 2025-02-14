import logging
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class LogHandler(logging.Handler):
    def __init__(self, label, max_lines=20):
        super().__init__()
        self.label = label  # 保存 QLabel 引用
        self.max_lines = max_lines  # 最大日志行数

    def emit(self, record):
        log_message = self.format(record)
        current_text = self.label.text()

        # 将新日志追加到当前文本
        new_text = current_text + "\n" + log_message if current_text else log_message

        # 检查行数是否超过最大值
        lines = new_text.split("\n")
        if len(lines) > self.max_lines:
            # 只保留最新的 max_lines 行
            new_text = "\n".join(lines[-self.max_lines:])

        # 更新 QLabel 的文本
        self.label.setText(new_text)

def get_logger(label, name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # 检查是否已经有处理器，避免重复添加
    if not logger.handlers:
        # 创建并设置自定义的 LogHandler
        handler = LogHandler(label, max_lines=10)  # 传递 log_label 和 max_lines
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
class LogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日志窗口")
        self.setFixedSize(400, 300)

        # 创建布局
        layout = QVBoxLayout(self)

        # 创建 QLabel 来显示日志
        self.log_label = QLabel(self)
        self.log_label.setText("日志输出：")
        layout.addWidget(self.log_label)

        # 设置 logging 配置
        self.setup_logging()

    def setup_logging(self):
        # 创建 LogHandler，指定输出到 QLabel
        log_handler = LogHandler(self.log_label)

        # 设置 logging 格式
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_handler.setFormatter(log_formatter)

        # 配置 logging
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.DEBUG)

        # 测试输出日志
        logging.debug("这是调试信息")
        logging.info("这是信息日志")
        logging.warning("这是警告日志")
        logging.error("这是错误日志")
        logging.critical("这是严重错误日志")

if __name__ == "__main__":
    app = QApplication([])

    window = LogWindow()
    window.show()

    app.exec()
