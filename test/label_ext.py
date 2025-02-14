import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QLinearGradient, QColor
from PySide6.QtCore import Qt, QPoint


class GradientLabel(QLabel):
    def paintEvent(self, event):
        # 创建QPainter对象
        painter = QPainter(self)

        # 定义渐变区域（从左上到右下）
        rect = self.rect()
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        color1 = '157,150,179'
        color2 = '255,198,123'
        # 设置颜色停靠点（0.0为起点颜色，1.0为终点颜色）
        gradient.setColorAt(0.0, QColor(230,133, 57))  # 更深的金色
        gradient.setColorAt(1.0, QColor(20, 90, 155))  # 更深的蓝色

        # 使用渐变填充背景
        painter.fillRect(rect, gradient)

        # 调用父类方法绘制文本（确保文本在背景之上）
        super().paintEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gradient Label Example")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        # 创建渐变Label并设置文本属性
        label = GradientLabel("Hello, Gradient Background!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: white;")  # 设置文本颜色为白色

        layout.addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())