# from PyQt5.QtWidgets import*
from PyQt5 import QtWidgets, QtGui, QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

    
class MplWidget(QtWidgets.QWidget):
    
    def __init__(self, parent = None):

        QtWidgets.QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.installEventFilter(self)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)


    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton:
                pass
                # print("Simple mouse motion")
            elif event.buttons() == QtCore.Qt.LeftButton:
                print("Left click drag")
            elif event.buttons() == QtCore.Qt.RightButton:
                print("Right click drag")
        elif event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                print("Press! x = " + str(MplWidget.x) + "; y = " + str(MplWidget.y))
        return super(MplWidget, self).eventFilter(source, event)
