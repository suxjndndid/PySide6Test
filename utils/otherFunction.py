import cv2
import numpy as np
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap, Qt, QPainter, QBrush, QPainterPath
from PySide6.QtWidgets import QApplication
from 景区慧手.utils import log_ext
from 景区慧手.utils.webCamera import WebcamThread, Camera

class other_Function:
    threads = []  # 新增类变量保存所有线程
    page = 0
    cams = [0]  # 确保cams已初始化
    trsp = []
    labels_list = []
    now_label = 0
    logging = None
    @staticmethod
    def imgToLabel(cam, label):
        try:
            thread = WebcamThread(cam)
            thread.changePixmap.connect(lambda frame: other_Function.showImg_all(frame, label))
            other_Function.threads.append(thread)  # 保存线程引用
            thread.start()
        except Exception as e:
            other_Function.logging.error(f"imgToLabel错误: {e}")

    @staticmethod
    def stop_all_threads():
        for thread in other_Function.threads:
            thread.stop()
        other_Function.threads.clear()
    @staticmethod
    def showImg(frame, label):
        try:
            # 获取 QLabel 的大小
            label_width = label.geometry().width()
            label_height = label.geometry().height()

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
            label.setPixmap(QPixmap.fromImage(q_image))

        except Exception as e:
            other_Function.logging.error(f"Error in update_image: {e}")
    @staticmethod
    def showImg_all(frame, label, border_size=10):
        try:
            # 获取 QLabel 的大小
            label_width = label.geometry().width()
            label_height = label.geometry().height()

            # 将捕获的帧转换为 RGB 格式
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape

            # 将图像转换为 QImage 格式
            q_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)

            # 计算图像需要裁剪的宽度差
            aspect_ratio = w / h
            label_aspect_ratio = label_width / label_height

            # 根据宽高比决定如何调整图像
            if aspect_ratio > label_aspect_ratio:
                # 如果图像更宽，裁剪左右两边
                new_width = int(label_height * aspect_ratio)
                offset_x = (new_width - label_width) // 2
                pixmap = QPixmap.fromImage(q_image).scaled(new_width, label_height, Qt.KeepAspectRatioByExpanding,
                                                           Qt.SmoothTransformation)
                pixmap = pixmap.copy(offset_x, 0, label_width, label_height)
            else:
                # 如果图像更高，裁剪上下两边
                new_height = int(label_width / aspect_ratio)
                offset_y = (new_height - label_height) // 2
                pixmap = QPixmap.fromImage(q_image).scaled(label_width, new_height, Qt.KeepAspectRatioByExpanding,
                                                           Qt.SmoothTransformation)
                pixmap = pixmap.copy(0, offset_y, label_width, label_height)

            # 创建一个透明的 QPixmap，大小为 QLabel 的尺寸
            rounded_pixmap = QPixmap(label_width, label_height)
            rounded_pixmap.fill(Qt.transparent)

            # 使用 QPainter 来绘制图像
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)  # 开启抗锯齿

            # 使用 QPainterPath 创建带圆角的矩形路径
            path = QPainterPath()
            path.addRoundedRect(border_size, border_size, label_width - 2 * border_size, label_height - 2 * border_size,
                                15, 15)  # 15 是圆角半径

            # 裁剪路径并绘制图像
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, pixmap)

            painter.end()

            # 显示带圆角且留有边距的图像到 QLabel 上
            label.setPixmap(rounded_pixmap)

        except Exception as e:
            other_Function.logging.error(f"Error in showImg: {e}")

    # 新增方法，用于批量渲染摄像头画面
    @staticmethod
    def renderCameras(labels, page=0):
        other_Function.logging.info("renderCameras函数开始运行")
        # other_Function.imgToLabel(0, labels[3])
        if not other_Function.cams:
            logging.warning("摄像头列表为空")
            return
        if not labels:
            logging.warning("标签列表为空")
            return
        for i, cam in enumerate(other_Function.cams[page * 4:(page + 1) * 4]):
            other_Function.logging.info(f"正在处理第{i}个摄像头{cam}")
            if i < len(labels):  # 确保不会超出cams的范围
                other_Function.logging.info(f"正在渲染第{i}个摄像头")
                other_Function.imgToLabel(i, labels[i])
            else:
                logging.warning(f"第{i}个摄像头超出范围")

    @staticmethod
    def showQF(display_text, target_num, sum_value, model_name, labels):
        # 设置标签的文本并居中显示
        global logging
        labels[0].setText(display_text)
        labels[0].setAlignment(Qt.AlignCenter)  # 居中显示文本

        labels[1].setText(target_num)
        labels[1].setAlignment(Qt.AlignCenter)  # 居中显示文本

        labels[2].setText(sum_value)
        labels[2].setAlignment(Qt.AlignCenter)  # 居中显示文本

        labels[3].setText(model_name)
        labels[3].setAlignment(Qt.AlignCenter)  # 居中显示文本


    @staticmethod
    def load_rust_webcam():
        pass

    @staticmethod
    def stop_webcam():
        for thread in other_Function.threads:
            thread.stop()
            thread.quit()
            thread.wait()
        other_Function.threads = []
        QTimer.singleShot(100, other_Function.clear_labels)
    @staticmethod
    def stop():
        other_Function.stop_webcam()

    @staticmethod
    def clear_labels():
        for label in other_Function.labels_list:
            label_width = label.width()
            label_height = label.height()

            # 使用透明 QPixmap 清除图像
            transparent_pixmap = QPixmap(label_width, label_height)
            transparent_pixmap.fill(Qt.transparent)

            # 清除 QLabel 内容
            label.clear()

            # 设置透明图像到 QLabel
            label.setPixmap(transparent_pixmap)

            # 强制刷新界面
            label.repaint()
            QApplication.processEvents()

            # 如果有父组件，刷新父组件
            if label.parent():
                label.parent().update()
    @staticmethod
    def to_label():
        other_Function.logging.info("to_label函数开始运行")
        other_Function.stop_webcam()
        other_Function.imgToLabel(0, other_Function.labels_list[other_Function.now_label])

    @staticmethod
    def next_l():
        other_Function.logging.info("next_l函数开始运行")
        other_Function.now_label =(other_Function.now_label+1) % 4
        other_Function.to_label()
    @staticmethod
    def pre_l():
        other_Function.logging.info("pre_l函数开始运行")
        other_Function.now_label =(other_Function.now_label-1+4) % 4
        other_Function.to_label()
    @staticmethod
    def set_log(log):
        other_Function.logging = log

if __name__ == '__main__':
    bf = other_Function()
    bf.renderCameras('video1')
