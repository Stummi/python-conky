#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QImage
from PyQt5.QtCore import Qt, QTimer

logger = logging.getLogger(__name__)

class fillbar(QWidget):
    """
    """
    def __init__(self, data_source, parent = None, redraw_interval=None, max_range=100, min_range=0):
        r"""
        Parameters:
         - data_source - a function reference that returns a numeric value on,
           that value will be used to plot the graph
         - redraw_interval - if set causes the widget to call its update method
           periodically, to update its own appearance, defaults to None,
           disabling independent update, which in effect causes this widget
           to only update itself with the main window
         - max_range and min_range - the upper und lower bound for the bars value defaults to 100 and 0 

        >>> app = QApplication(sys.argv)
        >>> static = lambda : 1
        >>> static_plot = plot(static, data_interval=100)
        """
        super(fillbar, self).__init__(parent = parent)
        self.palette().Background = QColor(255, 0, 0)
        self.border_color = QColor(255, 0, 0)
        self.bar_color = QColor(0, 255, 0)
        self.orientation  = 'horizontal'
        self.data_source = data_source
        self.max_range = max_range
        self.min_range = min_range
        
        self.initTimers(redraw_interval)

        self.show()
        
    def initTimers(self, redraw_interval):
        if redraw_interval:
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.update)
            self.update_timer.start(redraw_interval)

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

        #draw bar
        width  -= 2
        height -= 2
        value = orig_value = self.data_source()
        value = min(self.max_range, value)
        value = max(self.min_range, value)
        qp.setPen(self.bar_color)
        qp.setBrush(self.bar_color)
        if self.orientation == 'horizontal':
            qp.drawRect(1, 1,
                        width / self.max_range * value, height)
        else:
            qp.drawRect(1, height - (height / self.max_range * value), width, height)
        qp.setPen(self.border_color)
        qp.drawText(event.rect(), Qt.AlignCenter, str(orig_value))
        qp.end()
        logger.debug("paintEvent End: {0}".format(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
