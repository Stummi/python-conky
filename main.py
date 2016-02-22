#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
deps:
  python3 python3-psutil python3-pyqt5

may also use python-mpd, but it seems that debian packages that module only for 
python2, manual install via pip(pip3 on debian) required

"""

import sys
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

import platform
import psutil
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
import widgets

import argparse
parser = argparse.ArgumentParser(description="A more flexible replacement for conky written in python")
parser.add_argument("-c", "--config", help="path to the configuration file" )
args = parser.parse_args()

import os.path
config_path = args.config or "~/.python-conkyrc"
config_path = os.path.expanduser(config_path)
config_str = ''
with open(config_path, 'rb') as config_file:
    config_str = config_file.read()
exec(config_str)
        
config = Config()

class SysInfo():
    import platform
    print(platform.uname(), platform.system_alias(platform.system(), platform.release(), platform.version()))

    import psutil
    psutil.boot_time()
    psutil.cpu_count(logical=False)
    psutil.cpu_percent(percpu=True)    

class MainWin(QMainWindow):
    
    def __init__(self):
        super(QMainWindow, self).__init__(None, Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint)
        self.initUI()
        config.initUI(self)
        self.initTimer()
        
    def initUI(self):
        if(config.realTransparency):
            self.setAttribute(Qt.WA_NoSystemBackground, True)
            self.setAttribute(Qt.WA_TranslucentBackground, True)  
            #self.setAttribute(Qt.WA_PaintOnScreen, True)
            self.setWindowOpacity(config.windowOpacity)
        self.setGeometry(*config.windowGeometry)
        self.setWindowTitle(config.windowTitle)
        self.show()

    def initTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(config.updateInterval)

    def drawBackground(self, event, painter):
        background = QPixmap("/home/mkl/Bilder/debian_red_metal_hex_by_monkeymagico.jpg")        
        painter.drawPixmap(event.rect(), background)
        
    def paintEvent(self, event):
        logger.debug("paintEvent: {0} - {1}".format(self, event.rect()))
        qp = QPainter()
        qp.begin(self)
        if not config.realTransparency:
            self.drawBackground(event, qp)
        qp.end()
        logger.debug("paintEvent End: " + str(self))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWin()
    sys.exit(app.exec_())

