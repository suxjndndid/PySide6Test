from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu
from PySide6.QtGui import QImage, QPixmap, QColor
from PySide6.QtCore import QTimer, QThread, Signal, QObject, QPoint, Qt
from ui.CustomMessageBox import MessageBox
from ui.home import Ui_MainWindow
# from utils.capnums import Camera
from ui.utils.UIFunctions import *
import json
import sys
import cv2
import os

from 景区慧手.utils import  log_ext
from 景区慧手.utils.otherFunction import other_Function
from 景区慧手.utils.showQF_ext import ShowQfThread
log = None
class MainWindow(QMainWindow, Ui_MainWindow):
    global log
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # basic interface
        self.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground)  # rounded transparent
        self.setWindowFlags(Qt.FramelessWindowHint)  # Set window flag: hide window borders
        UIFuncitons.uiDefinitions(self)
        # Show module shadows
        UIFuncitons.shadow_style(self, self.Time_QF, QColor(162, 129, 247))
        UIFuncitons.shadow_style(self, self.FLow_QF, QColor(251, 157, 139))
        UIFuncitons.shadow_style(self, self.Sum_QF, QColor(170, 128, 213))
        UIFuncitons.shadow_style(self, self.Model_QF, QColor(64, 186, 193))


        qf_labels = [
            self.nowTime,  # Time QLabel
            self.Target_num,  # Flow QLabel
            self.Sum,  # Sum QLabel
            self.Model_name  # Model QLabel
        ]
        self.ShowQfThread = ShowQfThread()
        self.ShowQfThread.data_update_inf.connect(lambda display_text, target_num, sum_value, model_name:
                                                  other_Function.showQF(display_text, target_num, sum_value, model_name,
                                                                        qf_labels))        # button connect
        self.ShowQfThread.start()
        self.ToggleBotton.clicked.connect(lambda: UIFuncitons.toggleMenu(self, True))   # left navigation button
        self.settings_button.clicked.connect(lambda: UIFuncitons.settingBox(self, True))   # top right settings button
        self.now_page = self.page1
        self.labels = [
            self.video1,  # video1 QLabel
            self.video2,  # video2 QLabel
            self.video3,  # video3 QLabel
            self.video4  # video4 QLabel
        ]
        other_Function.labels_list = self.labels
        self.cam_page = 0
        # self.run_button.clicked.connect(lambda: other_Function.renderCameras(self.labels, self.cam_page))
        self.run_button.clicked.connect(lambda: other_Function.to_label())
        self.turnToPage2.clicked.connect(lambda: self.switch_to_page(self.page2))
        self.src_rtsp_button.clicked.connect(lambda: self.switch_to_page(self.page1))
        # 连接close按钮
        self.stop_button.clicked.connect(lambda: other_Function.stop())
        self.pre_page_button.clicked.connect(lambda: other_Function.pre_l())
        self.next_page_button.clicked.connect(lambda: other_Function.next_l())

        self.logger = log_ext.get_logger(self.show_log, "main")
        other_Function.set_log(self.logger)
    # Get the mouse position (used to hold down the title bar and drag the window)
    def mousePressEvent(self, event):
        p = event.globalPosition()
        globalPos = p.toPoint()
        self.dragPos = globalPos

    # Optimize the adjustment when dragging the bottom and right edges of the window size
    def resizeEvent(self, event):
        # Update Size Grips
        UIFuncitons.resize_grips(self)

    def switch_to_page(self, page):
        self.stackedWidget.setCurrentWidget(page)
    def close(self):
        self.logger.info("close 函数运行")
        other_Function.stop_webcam()
        super().close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    Home = MainWindow()
    Home.show()
    sys.exit(app.exec())  
