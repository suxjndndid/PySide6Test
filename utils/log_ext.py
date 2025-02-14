import logging
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class LogHandler(logging.Handler):
    def __init__(self, label):
        super().__init__()
        self.label = label

    def emit(self, record):
        log_message = self.format(record)
        current_text = self.label.text()
        new_text = current_text + "\n" + log_message
        self.label.setText(new_text)

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
