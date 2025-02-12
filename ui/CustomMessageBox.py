import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QApplication


# Single-button dialog box, which disappears automatically after appearing for a specified period of time
class MessageBox(QMessageBox):
    def __init__(self, *args, title='提示', count=1, time=1000, auto=False, **kwargs):
        super(MessageBox, self).__init__(*args, **kwargs)
        self._count = count
        self._time = time
        self._auto = auto  # Whether to close automatically
        assert count > 0  # must be greater than 0
        assert time >= 500  # Must be >=500 milliseconds
        self.setStyleSheet('''
                            QWidget{
                                color: black;
                                background-color: qlineargradient(x0:0, y0:1, x1:1, y1:1, stop:0.4 rgb(107, 128, 210), stop:1 rgb(180, 140, 255));
                                font: 13pt "Microsoft YaHei UI";
                                padding-right: 5px;
                                padding-top: 14px;
                                font-weight: light;
                                border-radius: 10px;
                                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                            }
                            QLabel{
                                color: white;
                                background-color: rgba(107, 128, 210, 0);
                            }
                            QPushButton{
                                background-color: rgb(106, 132, 211);
                                color: white;
                                border-radius: 5px;
                                padding: 5px 10px;
                                font-size: 12pt;
                            }
                            QPushButton:hover{
                                background-color: rgb(85, 110, 176);
                            }
                            QPushButton:pressed{
                                background-color: rgb(65, 85, 131);
                            }
                            ''')
        self.setWindowTitle(title)

        self.setStandardButtons(QMessageBox.StandardButton.Close)  # close button
        self.closeBtn = self.button(QMessageBox.StandardButton.Close)  # get close button
        self.closeBtn.setText('Close')
        self.closeBtn.setVisible(False)
        self._timer = QTimer(self, timeout=self.doCountDown)
        self._timer.start(self._time)

    def doCountDown(self):
        self._count -= 1
        if self._count <= 0:
            self._timer.stop()
            if self._auto:  # auto close
                self.accept()
                self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建 QApplication 实例
    msg_box = MessageBox(text='GGBond', title='提示', time=10000, auto=True)
    msg_box.exec()
    sys.exit(app.exec())  # 启动事件循环
