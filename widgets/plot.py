#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import collections
import logging
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPalette
from PyQt5.QtCore import Qt, QTimer, QPoint

logger = logging.getLogger(__name__)

class plot(QWidget):
    """
    A QWidget that periodically querys a function for data which it plots
    in a basic graph filling its whole drawing surface    
    """
    def __init__(self, data_source, parent = None, data_interval = 1000, redraw_interval = None):
        r"""
        Parameters:
         - data_source - a function reference that returns a numeric value on,
           that value will be used to plot the graph
         - data_interval - the interval in milliseconds between two calls to 
           data_source, in effect the time resolution of the resulting plot,
           defaults to 1000(1s)
         - redraw_interval - if set causes the widget to call its update method
           periodically, to update its own appearance, defaults to None,
           disabling independent update, which in effect causes this widget
           to only update itself with the main window

        >>> app = QApplication(sys.argv)
        >>> static = lambda : 1
        >>> static_plot = plot(static, data_interval=100)
        """
        super(plot, self).__init__(parent = parent)
        self.border_color = self.palette().color(QPalette.Window)
        self.plot_color = self.palette().color(QPalette.Text)
        self.data_source = data_source

        self.data = collections.deque(maxlen=100)
        
        self.initTimers(data_interval, redraw_interval)

        self.show()
        
    def initTimers(self, data_interval, redraw_interval):
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.query_data)
        self.data_timer.start(data_interval)
        if redraw_interval:
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.update)
            self.update_timer.start(redraw_interval)

    def query_data(self):
        logger.debug("query_data: {0}".format(self))
        self.data.append(self.data_source())
        logger.debug("query_data End: {0}".format(self))

    def paintEvent(self, event):
        logger.debug("paintEvent: {0} - {1}".format(self, event.rect()))
        qp = QPainter()
        qp.begin(self)
        
        width = self.size().width() - 1 
        height = self.size().height() - 1 

        #draw border
        qp.setPen(self.border_color)
        qp.drawLine(0, 0, width, 0)
        qp.drawLine(0, 0, 0, height)
        qp.drawLine(width, 0, width, height)
        qp.drawLine(0, height, width, height)

        #draw plot
        width  -= 1
        height -= 1 
        if len(self.data):
            qp.setPen(self.plot_color)
            max_val = max(self.data)
            points = list();
            for index in range(len(self.data)-1, 1, -1):
                points.append(QPoint((width / 100 * index),       height - (height / max_val * self.data[index])))
            points.append(QPoint(1,     height))
            points.append(QPoint(width, height))
            qp.setBrush(self.plot_color)
            qp.drawPolygon(*points)
        qp.end()
        logger.debug("paintEvent End: {0}".format(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
