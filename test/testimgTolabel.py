# test/test_imgToLabel.py

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QSizePolicy
from 景区慧手.utils.otherFunction import other_Function

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("测试 imgToLabel 方法")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # 创建一个 QLabel 来显示视频流
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置大小策略为可扩展
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        # 调用 imgToLabel 方法
        other_Function.imgToLabel(0, self.label)  # 假设使用摄像头设备号 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
