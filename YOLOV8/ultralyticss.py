from ultralytics import YOLO
import cv2
import numpy as np
from PyQt5.QtGui import QImage,QPixmap, QImageWriter
from PyQt5.QtCore import Qt, QTimer,pyqtSignal,pyqtSlot,QObject,QByteArray
from typing import Union
import os

class Ultralyticss(QObject):

    VCsignal = pyqtSignal(QPixmap)
    #
    def detect(self,Model_Path:str,Image_Path:str):
        self.model = YOLO(Model_Path)
        '''
        source :图片
        show:是否显示
        save:保存--runs/detect文件中
        '''
        result =self.model.predict(source=Image_Path,show=False,save=True,epochs = 3)
        result_image = result[0].plot()
        cv2.imwrite('./result.jpg',result_image)
        pixmap = QPixmap.fromImage(QImage('./result.jpg'))
        
        return pixmap
    
    def data(self):
        os.system("labelImg")
    
    def VideoCapture(self,Model_Path:str,Camera_No,timeout:int):
        self.model = YOLO(Model_Path)
        self.timer = QTimer(self)
        self.timer.timeout.connect(slot=self.update_frame)
        self.cap = cv2.VideoCapture(Camera_No)
        self.timer.start(timeout)

    
    def update_frame(self):
        ret,frame = self.cap.read()
        if not ret:
            return
        result = self.model(frame)
        annotated_frame = result[0].plot()
        cv2.imwrite('./result.jpg',annotated_frame)
        pixmap = QPixmap.fromImage(QImage('./result.jpg'))

        self.VCsignal.emit(pixmap)
    
    def VideoCapture_Stop(self):
        self.timer.stop()
        self.cap.release()

    def Track(self,Model_Path:str,source:str,timeout:int):
        self.model = YOLO(Model_Path)
        self.cap = cv2.VideoCapture(source)
        self.VCRtimer =QTimer(self)
        self.VCRtimer.timeout.connect(slot=self.VCR_update_frame)
        self.VCRtimer.start(timeout)


    def VCR_update_frame(self):
        ret,frame = self.cap.read()
        if not ret:
            return
        result = self.model(frame)
        annotated_frame = result[0].plot()
        cv2.imwrite('./result.jpg',annotated_frame)
        pixmap = QPixmap.fromImage(QImage('./result.jpg'))
        self.VCsignal.emit(pixmap)

    def DeletJpg(self):
        if os.path.exists('./result.jpg'):
            os.remove('./result.jpg')
        else:
            pass
    
    def trains(self,Model_path:str,Data_Path:str,epochs:int,imgsz:int) ->Union[None, str]:
        '''
        data:为.yaml格式
        epochs:训练轮数，多为50-200
        imgsz:图像（像素）大小
        '''
        try:
            self.model = YOLO(Model_path)
            self.model.train(data=Data_Path,epochs=epochs, imgsz=imgsz)
        except Exception as e:
            return str(e)