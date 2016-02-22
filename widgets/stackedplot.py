#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import collections
import logging

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QImage
from PyQt5.QtCore import Qt, QTimer, QPoint

import widgets

logger = logging.getLogger(__name__)

class stackedplot(widgets.plot):
    """
     
    """
    def __init__(self, data_source, num_data_points, parent = None, data_interval=1000, redraw_interval=None):
        r"""
        Parameters:
         - data_source - a function reference that returns a collection of numeric values
         - num_data_points - the number of values the data_source should return
           on each call, if it returns more than that, the rest are ignored.
           if it returns less, all are discarded
         - data_interval - the interval in milliseconds between two calls to 
           data_source, in effect the time resolution of the resulting plot,
           defaults to 1000(1s)
         - redraw_interval - if set causes the widget to call its update method
           periodically, to update its own appearance, defaults to None,
           disabling independent update, which in effect causes this widget
           to only update itself with the main window

        >>> app = QApplication(sys.argv)
        >>> static = lambda : (1,2,3)
        >>> static_plot = plot(static, 3, data_interval=100)
        """
        super(stackedplot, self).__init__(data_source = data_source, parent = parent, data_interval = data_interval, redraw_interval = redraw_interval)

        self.plot_colors = (QColor(255,0,0), QColor(0,255,0), QColor(0,0,255), QColor(0,0,0))
        
        self.num_data_points = num_data_points
        
    def query_data(self):
        logger.debug("query_data: {0}".format(self))
        result = self.data_source()
        result = result[:self.num_data_points]
        if(len(result) == self.num_data_points ):
            add_result = list()
            for c1 in range(len(result)):
                add_result.append(sum(result[:c1+1]))
            self.data.append(add_result)
        else:
            logger.warn("query_data result to short: {0}".format(result))
        logger.debug("query_data End: {0}".format(self))

    def paintEvent(self, event):
        logger.debug("paintEvent: {0} - {1}".format(self, event.rect()))
        qp = QPainter()
        qp.begin(self)
        
        width = self.size().width() - 1 
        height = self.size().height() - 1 

        #draw border
        qp.setPen(self.border_color)
        qp.drawRect(0,0, width, height)
        
        #draw plot
        width  -= 1
        height -= 1
        if len(self.data):
            max_val = max(map(lambda x: x[-1], self.data))
            plots = [list() for _ in range(self.num_data_points) ]
            for index in range(len(self.data)-1, 1, -1):
                for inner_index in range(self.num_data_points):
                    plots[inner_index].append(QPoint((width / self.data.maxlen * index),
                                                     height - (height / max_val * self.data[index][inner_index])))
            for x in range(len(plots)-1, -1, -1):
                qp.setPen(self.plot_colors[x])
                qp.setBrush(self.plot_colors[x])
                points = plots[x]
                points.append(QPoint(1,     height))
                points.append(QPoint(width, height))
                qp.drawPolygon(*points)
        qp.end()
        logger.debug("paintEvent End: {0}".format(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
