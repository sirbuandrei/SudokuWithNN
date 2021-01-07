# LABEL USED FOR SHOWING THE PREDICTION
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont


class BlankLabel(QtWidgets.QLabel):
    def __init__(self, value, x, y, i, j, parent=None):
        super(BlankLabel, self).__init__(parent=parent)
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.value = str(value)
        self.parent = parent
        self.setStyleSheet("QLabel{\n"
                           "    background: white;\n"
                           "}")
        self.setGeometry(x, y, 41, 41)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont('Century Gothic', 20))
        self.setText(self.value)
        self.delete = False

    def mouseReleaseEvent(self, event):
        # IF THE LABEL IS CLICKED POTENTIAL DELETE (MUST WAIT FOR SPACE TO BE PRESSED)
        if event.button() == Qt.LeftButton:
            self.delete = True
