import logging

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QLabel

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QLabel
import time
import random



class ShowQfThread(QThread):
    data_update_inf = Signal(str, str, str, str)
    def __init__(self, interval=60, parent=None):
        super().__init__(parent)
        self.update_increase_time = interval  # 传入的更新间隔时间（分钟）
        self.sum_pre = 0
        self.increase_value = 0
        self.model_name = "None"
        self.model_name_pre = "None"
        self.sum_value = 0
        self.sum_value_pre = 0
        self.running = True  # 控制线程是否持续运行
        self.last_increase_update_time = time.time()  # 上次更新 `increase_value` 的时间

    def run(self):
        while self.running:
            # 自动更新时间
            current_time = time.time()  # 获取当前时间戳
            display_text = time.strftime("%H:%M:%S", time.localtime(current_time))  # 当前时间

            # 检查是否到了更新 `increase_value` 的时间
            if (current_time - self.last_increase_update_time) >= (
                    self.update_increase_time * 60):  # `interval` 为分钟
                self.increase_value = self.sum_value - self.sum_pre
                self.sum_pre = self.sum_value
                self.last_increase_update_time = current_time  # 更新最后一次更新的时间

            # 更新值比较
            if self.model_name != self.model_name_pre:
                self.model_name_pre = self.model_name
            if self.sum_value != self.sum_value_pre:
                self.sum_value_pre = self.sum_value

            # 发射信号更新数据
            self.data_update_inf.emit(display_text, str(self.sum_value), str(self.increase_value), self.model_name)
            time.sleep(1)  # 每秒更新一次时间


    def update_data(self,  model_name=None, sum_value=None):
            if model_name is not None:
                self.model_name = model_name
            if sum_value is not None:
                self.sum_value = sum_value