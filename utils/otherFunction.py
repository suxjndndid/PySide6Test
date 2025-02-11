import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap

from 景区慧手.utils.webCamera import WebcamThread, Camera
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class other_Function:
    threads = []  # 新增类变量保存所有线程
    page = 0
    cams = [0]  # 确保cams已初始化

    @staticmethod
    def imgToLabel(cam, label):
        try:
            logging.info(f"启动摄像头{cam}到标签")
            # 检查摄像头是否可用
            camera_checker = Camera(cam_preset_num=cam + 1)
            count, devices = camera_checker.get_cam_num()
            if cam not in devices:
                logging.error(f"摄像头{cam}不可用")
                return

            thread = WebcamThread(cam)
            thread.changePixmap.connect(lambda frame: other_Function.showImg(frame, label))
            other_Function.threads.append(thread)  # 保存线程引用
            thread.start()
        except Exception as e:
            logging.error(f"imgToLabel错误: {e}")

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
            logging.error(f"Error in update_image: {e}")
    # 新增方法，用于批量渲染摄像头画面
    @staticmethod
    def renderCameras(labels, page=0):
        logging.info("renderCameras函数开始运行")
        other_Function.imgToLabel(0, labels[0])
        if not other_Function.cams:
            logging.warning("摄像头列表为空")
            return
        if not labels:
            logging.warning("标签列表为空")
            return
        # for i, cam in enumerate(other_Function.cams[page * 4:(page + 1) * 4]):
        #     logging.info(f"正在处理第{i}个摄像头{cam}")
        #     if i < len(labels):  # 确保不会超出cams的范围
        #         logging.info(f"正在渲染第{i}个摄像头")
        #         other_Function.imgToLabel(i, labels[i])
        #     else:
        #         logging.warning(f"第{i}个摄像头超出范围")

    @staticmethod
    def showQF(info, label):
        label.setText(info)


    @staticmethod
    def load_rust_webcam():
        # 假设这里加载Rust摄像头
        for i in range(4):  # 假设有4个Rust摄像头
            cam = WebcamThread(i)  # 创建WebcamThread对象
            other_Function.cams.append(cam)  # 将摄像头添加到cams列表中


if __name__ == '__main__':
    bf = other_Function()
    bf.renderCameras('video1')
