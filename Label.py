# LABEL USED FOR DRAWING
from PyQt5 import QtWidgets
from keras.models import load_model
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, qRgb
from PIL import ImageGrab
import SudokuSolver as ss
from SudokuSolver import grid
import win32gui
import numpy as np
import datetime

previous = None
labels = []
blank_labels = []

# LOAD TRAINED MODEL
model = load_model('model')


def predict(img):
    # RESIZE THE IMAGE
    img = img.resize((28, 28))
    # CONVERT TO GRAY SCALE
    img = img.convert('L')
    # CONVERT IMAGE INTO NP.ARRAY
    img = np.array(img)
    # RESHAPE THE IMAGE
    img = img.reshape((-1, 784))
    # GET THE OUTPUT ARRAY
    res = model.predict([img])[0]
    return np.argmax(res)


# SET THE BLANK LABEL TEXT TO THE PREDICTED VALUE
def place_prediction(label):
    # GET THE IMG FROM PREVIOUS LABEL
    HWND = label.winId()
    rect = win32gui.GetWindowRect(HWND)
    im = ImageGrab.grab(rect)
    # FIND THE PREVIOUS LABEL TO UPDATE THE TEXT
    for bl in blank_labels:
        if bl.i == label.i and bl.j == label.j:
            # WHEN FIND IT SET TEXT FOR THE BLANK-LABEL TO THE VALUE PREDICTED AND ADD IT TO THE GRID
            value = predict(im)
            bl.setText(str(value))
            # IF THE VALUE DRAWN IS MISPLACED MAKE THE TEXT RED
            if not ss.checkvalue(bl.i, bl.j, value):
                bl.setStyleSheet("QLabel{\n"
                                 "    background: white;\n"
                                 "    color: red;\n"
                                 "}")

            # UPDATE THE GRID WITH THE VALUE
            grid[bl.i][bl.j] = value
    # CLEARING LABEL IN CASE OF DELETING BLANK-LABEL LATER AND HIDE IT
    label.delete = False
    label.pixmap.fill(Qt.white)
    label.hide()


class Label(QtWidgets.QLabel):
    def __init__(self, x, y, i, j, parent=None):
        super(Label, self).__init__(parent=parent)
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.parent = parent
        self.setStyleSheet("QLabel{\n"
                           "    background: (255, 229, 180);\n"
                           "    border: 2px solid black;    \n"
                           "}")
        self.setGeometry(x, y, 41, 41)
        # CREATE BLANK IMAGE AND ADD IT TO THE PIXMAP
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        self.image.fill(qRgb(255, 255, 255))
        self.pixmap = QPixmap.fromImage(self.image)
        self.setPixmap(self.pixmap)

    def mousePressEvent(self, event):
        global previous
        # IF LEFT MOUSE BUTTON IS PRESSED
        if event.button() == Qt.LeftButton:
            # IF WE BEGIN DRAWING ON ANOTHER LABEL
            if previous and previous != self:
                place_prediction(previous)
            # MAKE DRAWING FLAG FALSE
            self.drawing = True
            # MAKE LAST POINT THE CURRENT POINT OF CURSOR
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        # CHECKING IF LEFT BUTTON IS PRESSED AND DRAWING FLAG TRUE
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            # CREATING PAINTING OBJECT
            painter = QPainter(self.pixmap)
            # SET THE PEN OF THE PAINTER
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            # DRAW LINE FROM THE LAST POINT OF THE CURSOR TO THE CURRENT POINT
            painter.drawLine(self.lastPoint, event.pos())
            # UPDATE LAST POINT AND THE LABEL
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        global previous, finish
        if event.button() == Qt.LeftButton:
            # MAKE DRAWING FLAG FALSE
            self.drawing = False
            self.pixmap.scaled(41, 41, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # SET THE PREVIOUS LABEL TO THIS ONE AFTER FINISHING DRAWING
            previous = self

    def paintEvent(self, event):
        # CREATE CANVAS
        canvasPainter = QPainter(self)
        # CONSTANTLY DRAW THE PIXMAP (TO UPDATE WHAT YOU DREW)
        canvasPainter.drawPixmap(self.rect(), self.pixmap)
