import time

import cv2
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu

from webCamera import Camera, WebcamThread
from .ui.CustomMessageBox import MessageBox

from .otherFunction import baseFunction


class buttonFUntion:
    def __init__(self):
        super().__init__()
        self.stop = baseFunction.stop()
        self.starOrContinue = baseFunction.starOrCOntinue()
        self.showImg = baseFunction.showImg()
        self.cams = []
        self.labels = ['video1', 'video2', 'video3', 'video4']  # 假设这些是你的label对象
        self.page = 0  # 初始化页码

    def selectWebcam(self):
        try:
            self.stop()
            MessageBox(
                self.close_button, title='Note', text='loading camera...', time=2000, auto=True).exec()

            # get the number of local cameras
            cam_num, cams = Camera().get_cam_num()
            if cam_num > 0:
                popMenu = QMenu()
                popMenu.setFixedWidth(self.src_cam_button.width())
                popMenu.setStyleSheet('''... existing code ...''')

                for cam in cams:
                    exec("action_%s = QAction('%s')" % (cam, cam))
                    exec("popMenu.addAction(action_%s)" % cam)

                x = self.src_cam_button.mapToGlobal(self.src_cam_button.pos()).x()
                y = self.src_cam_button.mapToGlobal(self.src_cam_button.pos()).y()
                y = y + self.src_cam_button.frameGeometry().height()
                pos = QPoint(x, y)
                action = popMenu.exec(pos)
                if action:
                    self.cams.append(action.text())
                    self.show_status('Loading camera：{}'.format(action.text()))
            else:
                self.showStatus('No camera found !!!')
        except Exception as e:
            self.show_status('%s' % e)

    def startWebcam(self, page=0):
        self.page = page
        baseFunction().renderCameras(self.cams, self.labels, self.page)
