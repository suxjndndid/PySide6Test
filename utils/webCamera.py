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



