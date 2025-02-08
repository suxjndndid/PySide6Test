import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap

from 景区慧手.utils.webCamera import WebcamThread


class baseFunction:

    def stop(self, stop_status=False):
        for yolo_name in self.yolo_threads.threads_pool.keys():
            try:
                if stop_status:
                    self.yolo_threads.get(yolo_name).stop_dtc = True
                self.yolo_threads.stop_thread(yolo_name)
            except Exception as err:
                print(repr(err))

    def imgToLabel(self, cam, label):
        self.showStatus(f'Loading camera：Camera_{cam}')
        self.thread = WebcamThread(cam)
        self.thread.changePixmap.connect(lambda x: self.showImg(x, label, 'img'))
        self.thread.start()
        self.inputPath = int(cam)

    def showImg(self, img, label, flag):
        try:
            if flag == "path":
                img_src = cv2.imdecode(np.fromfile(img, dtype=np.uint8), -1)
            else:
                img_src = img
            ih, iw, _ = img_src.shape
            w = label.geometry().width()
            h = label.geometry().height()
            # keep original aspect ratio
            if iw / w > ih / h:
                scal = w / iw
                nw = w
                nh = int(scal * ih)
                img_src_ = cv2.resize(img_src, (nw, nh))
            else:
                scal = h / ih
                nw = int(scal * iw)
                nh = h
                img_src_ = cv2.resize(img_src, (nw, nh))

            frame = cv2.cvtColor(img_src_, cv2.COLOR_BGR2RGB)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[2] * frame.shape[1],
                         QImage.Format_RGB888)
            label.setPixmap(QPixmap.fromImage(img))
        except Exception as e:
            print(repr(e))

    # 新增方法，用于批量渲染摄像头画面
    def renderCameras(self, cams, labels, page=0):
        for i, cam in enumerate(cams[page*4:(page+1)*4]):
            if i < len(labels) :  # 确保不会超出cams的范围
                self.imgToLabel(cam, labels[i])

    def showQF(self, info, label):
        label.setText(info)