#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont, QImage
from PyQt5.QtCore import Qt, QTimer

import logging

def confLogging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

confLogging()

logger = logging.getLogger(__name__)


class Config:
    realTransparency = False
    windowTitle = 'python-conky'
    windowOpacity = 1.0
    windowGeometry = (300, 300, 280, 170)
    updateInterval = 1000

    def drawBackground(self, event, painter):
        background = QImage("/home/mkl/Bilder/debian_red_metal_hex_by_monkeymagico.jpg")
        painter.drawImage(0, 0, background)
    
    def draw(self, event, painter):
        painter.setPen(QColor(168, 34, 3, 255))
        painter.setFont(QFont('Terminus', 50))
        painter.drawText(event.rect(), Qt.AlignCenter, "Boring Random Text: üäö")
        painter.drawLine(20, 20, 1000, 20)
    
config = Config()

class SysInfo():
    import platform
    print(platform.uname(), platform.system_alias(platform.system(), platform.release(), platform.version()))

    

class MainWin(QMainWindow):
    
    def __init__(self):
        super(QMainWindow, self).__init__(None, Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint)
        self.initUI()
        self.initTimer()
                
    def initUI(self):
        if(config.realTransparency):
            self.setAttribute(Qt.WA_NoSystemBackground, True)
            self.setAttribute(Qt.WA_TranslucentBackground, True)  
            self.setAttribute(Qt.WA_PaintOnScreen, True)
            self.setWindowOpacity(config.windowOpacity)
        self.setGeometry(*config.windowGeometry)
        self.setWindowTitle(config.windowTitle)
        self.show()

    def initTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(config.updateInterval)

    def paintEvent(self, event):
        logger.debug("paintEvent: {0} - {1} - {2}".format(self, event.rect(), event.region().rects()))
        qp = QPainter()
        qp.begin(self)
        config.drawBackground(event, qp)
        config.draw(event, qp)
        qp.end()
        logger.debug("paintEvent End: " + str(self))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWin()
    sys.exit(app.exec_())

