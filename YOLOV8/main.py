from PyQt5.QtWidgets import QApplication,QWidget
import cv2
from PyQt5.QtGui import QIcon
import sys
from Widget import Ui_YOLOV8
#from ui import Ui_YOLOV8

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    ui = Ui_YOLOV8()
    ui.setupUi(window)
    window.setWindowIcon(QIcon('./YOLOV8.ico'))
    window.show()
    sys.exit(app.exec())
