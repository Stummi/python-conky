#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QImage
from PyQt5.QtCore import Qt, QTimer

class plot(QWidget):
    """
    A QWidget that periodically querys a function for data which it plots
    in a basic graph filling its whole drawing surface    
    """
    def __init__(self, data_source, data_interval=1000, redraw_interval=None):
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
        >>> static_plot = plot(static, 2000)
        
        """
        super(QWidget, self).__init__()
        
        self.initTimers(data_interval, redraw_interval)
        
    def initTimers(self, data_interval, redraw_interval):
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.query_data)
        self.data_timer.start(data_interval)
        if redraw_interval:
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.update())
            self.update_timer.start(redraw_interval)

    def query_data(self):
        pass

    def paintEvent(self, event):
        logger.debug("paintEvent: {0} - {1}".format(self, event.rect()))
        qp = QPainter()
        qp.begin(self)

        qp.end()
        logger.debug("paintEvent End: " + str(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
