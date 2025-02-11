import time

import cv2
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu

from 景区慧手.utils.webCamera import Camera, WebcamThread
from 景区慧手.ui.CustomMessageBox import MessageBox

from 景区慧手.utils.otherFunction import other_Function


class button_Function:
    page = 0  # 初始化页码

    @staticmethod
    def start_webcam(labels, page=0):
        logging.info(f"start_webcam开始运行, page: {page}")
        button_Function.page = page
        other_Function.renderCameras(labels, button_Function.page)


# 示例日志配置
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
