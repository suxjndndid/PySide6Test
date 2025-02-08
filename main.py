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
import 景区慧手.ui.resources


class MainWindow(QMainWindow, Ui_MainWindow):
    main2yolo_begin_sgl = Signal()  # The main window sends an execution signal to the yolo instance
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



        # Prompt window initialization
        self.Class_num.setText('--')
        self.Target_num.setText('--')
        self.fps_label.setText('--')
        self.Model_name.setText('--')
        
        # # Select detection source
        # self.src_file_button.clicked.connect(self.open_src_file)  # select local file
        # self.src_cam_button.clicked.connect(self.chose_cam)
        # # start testing button
        # self.run_button.clicked.connect(self.run_or_continue)   # pause/start
        # self.stop_button.clicked.connect(self.stop)             # termination
        #
        # # Other function buttons
        # self.save_res_button.toggled.connect(self.is_save_res)  # save image option
        # self.save_txt_button.toggled.connect(self.is_save_txt)  # Save label option
        # self.ToggleBotton.clicked.connect(lambda: UIFuncitons.toggleMenu(self, True))   # left navigation button
        # self.settings_button.clicked.connect(lambda: UIFuncitons.settingBox(self, True))   # top right settings button
        #
        # # initialization
        # self.load_config()

        self.turnToPage2.clicked.connect(lambda :self.switch_to_page(self.page2))
    # The main window displays the original image and detection results

    def load_config(self):
        config_file = 'config/setting.json'
        if not os.path.exists(config_file):
            iou = 0.26
            conf = 0.33   
            rate = 10
            save_res = 0   
            save_txt = 0    
            new_config = {"iou": iou,
                          "conf": conf,
                          "rate": rate,
                          "save_res": save_res,
                          "save_txt": save_txt
                          }
            new_json = json.dumps(new_config, ensure_ascii=False, indent=2)
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(new_json)
        else:
            config = json.load(open(config_file, 'r', encoding='utf-8'))
            if len(config) != 5:
                iou = 0.26
                conf = 0.33
                rate = 10
                save_res = 0
                save_txt = 0
            else:
                iou = config['iou']
                conf = config['conf']
                rate = config['rate']
                save_res = config['save_res']
                save_txt = config['save_txt']
        self.save_res_button.setCheckState(Qt.CheckState(save_res))
        self.yolo_predict.save_res = (False if save_res==0 else True )
        self.save_txt_button.setCheckState(Qt.CheckState(save_txt)) 
        self.yolo_predict.save_txt = (False if save_txt==0 else True )
        self.run_button.setChecked(False)  
        self.show_status("Welcome~")





    def ModelBoxRefre(self):
        pt_list = os.listdir('./models')
        pt_list = [file for file in pt_list if file.endswith('.pt')]
        pt_list.sort(key=lambda x: os.path.getsize('./models/' + x))
        # It must be sorted before comparing, otherwise the list will be refreshed all the time
        if pt_list != self.pt_list:
            self.pt_list = pt_list
            self.model_box.clear()
            self.model_box.addItems(self.pt_list)

    # Get the mouse position (used to hold down the title bar and drag the window)
    def mousePressEvent(self, event):
        p = event.globalPosition()
        globalPos = p.toPoint()
        self.dragPos = globalPos

    # Optimize the adjustment when dragging the bottom and right edges of the window size
    def resizeEvent(self, event):
        # Update Size Grips
        UIFuncitons.resize_grips(self)

    # Exit Exit thread, save settings
    def closeEvent(self, event):
        config_file = 'config/setting.json'
        config = dict()
        config['iou'] = self.iou_spinbox.value()
        config['conf'] = self.conf_spinbox.value()
        config['rate'] = self.speed_spinbox.value()
        config['save_res'] = (0 if self.save_res_button.checkState()==Qt.Unchecked else 2)
        config['save_txt'] = (0 if self.save_txt_button.checkState()==Qt.Unchecked else 2)
        config_json = json.dumps(config, ensure_ascii=False, indent=2)
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_json)
        # Exit the process before closing
        if self.yolo_thread.isRunning():
            self.yolo_predict.stop_dtc = True
            self.yolo_thread.quit()
            MessageBox(
                self.close_button, title='Note', text='Exiting, please wait...', time=3000, auto=True).exec()
            sys.exit(0)
        else:
            sys.exit(0)

    def switch_to_page(self, page):
        self.stackedWidget.setCurrentWidget(page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Home = MainWindow()
    Home.show()
    sys.exit(app.exec())  
