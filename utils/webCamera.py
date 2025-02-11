import sys
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtGui import QImage, Qt, QPixmap
from PySide6.QtCore import QThread, Signal
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Camera:
    def __init__(self, cam_preset_num=1):
        self.cam_preset_num = cam_preset_num

    def get_cam_num(self):
        cnt = 0
        devices = []
        for device in range(0, self.cam_preset_num):
            stream = cv2.VideoCapture(device)
            grabbed = stream.grab()
            stream.release()
            if not grabbed:
                continue
            else:
                cnt = cnt + 1
                devices.append(device)
        return cnt, devices

class WebcamThread(QThread):
    changePixmap = Signal(np.ndarray)

    def __init__(self, cam, parent=None):
        super().__init__(parent)
        self.cam = cam
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(self.cam)
        if not cap.isOpened():
            logging.error(f"无法打开摄像头设备 {self.cam}")
            return

        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                self.changePixmap.emit(frame)
            else:
                logging.error(f"无法读取摄像头帧 {self.cam}")
                break

        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("多线程摄像头测试")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # 创建一个label来显示视频流
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置大小策略为可扩展
        self.layout.addWidget(self.label)

        self.start_button = QPushButton("开始测试多摄像头", self)
        self.start_button.clicked.connect(self.start_cameras)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        self.camera = Camera(cam_preset_num=2)  # 设置最多检测2个摄像头

        # 设置窗口的最小大小
        self.setMinimumSize(400, 300)

    def start_cameras(self):
        cam_count, devices = self.camera.get_cam_num()
        logging.info(f"检测到 {cam_count} 个摄像头")

        if cam_count > 0:
            self.threads = []  # 保存线程对象

            for device in devices:
                webcam_thread = WebcamThread(device)
                webcam_thread.changePixmap.connect(self.update_image)
                self.threads.append(webcam_thread)
                webcam_thread.start()

    def update_image(self, frame):
        try:
            # 获取 QLabel 的大小
            label_width = self.label.geometry().width()
            label_height = self.label.geometry().height()

            # 将捕获的帧转换为 RGB 格式
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape

            # 计算图像缩放比例，保持原始纵横比
            if w / label_width > h / label_height:
                # 如果宽度比例大于高度比例，按宽度进行缩放
                scale = label_width / w
                new_w = label_width
                new_h = int(scale * h)
            else:
                # 否则按高度进行缩放
                scale = label_height / h
                new_w = int(scale * w)
                new_h = label_height

            # 使用 cv2.resize 进行缩放
            resized_image = cv2.resize(rgb_image, (new_w, new_h))

            # 将缩放后的图像转换为 QImage 格式
            q_image = QImage(resized_image.data, resized_image.shape[1], resized_image.shape[0],
                             resized_image.shape[2] * resized_image.shape[1], QImage.Format_RGB888)

            # 显示到 QLabel 上
            self.label.setPixmap(QPixmap.fromImage(q_image))

        except Exception as e:
            logging.error(f"Error in update_image: {e}")

    def closeEvent(self, event):
        # 停止所有线程
        if hasattr(self, 'threads'):
            for thread in self.threads:
                thread.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
