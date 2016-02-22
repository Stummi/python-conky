#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QImage
from PyQt5.QtCore import Qt, QTimer

logger = logging.getLogger(__name__)

class custom(QWidget):
    """
    """
    def __init__(self, parent = None, redraw_interval=None):
        r"""
        Parameters:
         - redraw_interval - if set causes the widget to call its update method
           periodically, to update its own appearance, defaults to None,
           disabling independent update, which in effect causes this widget
           to only update itself with the main window

        >>> app = QApplication(sys.argv)
        >>> static = lambda : 1
        >>> static_plot = plot(redraw_interval=5000)
        """
        super(custom, self).__init__(parent = parent)
        
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

        qp.setPen(self.border_color)
        qp.drawText(event.rect(), Qt.AlignCenter, "I was not subclassed, or paintEvent was not overwritten")

        qp.end()
        logger.debug("paintEvent End: {0}".format(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
