from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from 景区慧手.utils.otherFunction import other_Function

class MyWindow(QWidget):

    def custom_close(self):
        # 在这里实现你自己的关闭逻辑
        other_Function.stop()

        # 调用父类的 close 方法来实际关闭窗口
        self.close()


