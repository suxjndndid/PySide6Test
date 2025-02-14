from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtCore import QTimer, Qt


class LogWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("日志")
        self.setFixedSize(400, 300)

        # 设置布局
        layout = QVBoxLayout(self)

        # 日志标题
        title = QLabel("项目运行日志", self)
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # 日志内容显示区域
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("border: 1px solid #ddd;")
        layout.addWidget(self.log_output)

        # 模拟输出日志的按钮
        self.simulate_button = QPushButton("模拟输出日志", self)
        self.simulate_button.clicked.connect(self.simulate_log)
        layout.addWidget(self.simulate_button)

        # 定时器模拟日志输出
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simulate_log)

    def simulate_log(self):
        # 模拟生成日志信息
        log_message = "这是一个日志消息\n"

        # 获取当前文本并追加新的日志信息
        current_text = self.log_output.toPlainText()
        self.log_output.setPlainText(current_text + log_message)

        # 自动滚动到日志底部
        self.log_output.moveCursor(self.log_output.textCursor().End)


if __name__ == "__main__":
    app = QApplication([])

    window = LogWindow()
    window.show()

    app.exec()
