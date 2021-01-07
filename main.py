# SUDOKU GAME USING HANDWRITTEN IMAGE RECOGNITION
# THE IDEA OF THE GAME WAS TO HAVE 2 LABELS: ONE FOR DRAWING AND ONE FOR SHOWING THE VALUE DRAWN
# AFTER A VALUE IS DRAWN, HIDE THE DRAWING LABEL AND SET THE THE TEXT OF THE THE BLANK-LABEL TO THE VALUE DRAWN
# A VALUE IS SET WHEN ANOTHER LABEL BEGINS TO BE DRAWN
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Label import Label, labels, blank_labels, place_prediction
from BlankLabel import BlankLabel
import SudokuSolver as ss
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(450, 200, 600, 600)
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        self.setWindowTitle("Sudoku")
        self.setStyleSheet("QMainWindow{\n"
                           "background: rgb(255, 229, 180);\n"
                           "}")
        ss.get_grid()
        self.draw_board()

    def draw_board(self):
        for i in range(0, 9):
            for j in range(0, 9):
                # IF THE POS (I,J) ON THE GENERATED GRID IS EMPTY
                if ss.grid[i][j] == 0:
                    # PLACE THE BLANK LABEL
                    blank_labels.append(BlankLabel('', 100 + j * 41 + j * 2, 100 + i * 41 + i * 2, i, j, self))
                    labels.append(Label(100 + j * 41 + j * 2, 100 + i * 41 + i * 2, i, j, self))
                # IF NOT PLACE A LABEL WITH THE VALUE GENERATED
                else:
                    blank_labels.append(
                        BlankLabel(ss.grid[i][j], 100 + j * 41 + j * 2, 100 + i * 41 + i * 2, i, j, self))
                    # SET TEXT COLOR TO NAVY BLUE
                    blank_labels[-1].setStyleSheet("QLabel{\n"
                                                   "    background: white;\n"
                                                   "    color: rgb(56, 66, 84);\n"
                                                   "}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.gray, 4))

        # DRAW THE EDGE LINES OF THE SUDOKU GRID
        painter.drawLine(98, 98, 487, 98)
        painter.drawLine(98, 98, 98, 487)
        painter.drawLine(487, 98, 487, 487)
        painter.drawLine(98, 487, 487, 487)

        # DRAW THE IN BETWEEN LINES OF THE SUDOKU GRID
        for col in range(0, 9):
            painter.drawLine(100 + col * 41 + col * 2, 100, 100 + col * 41 + col * 2, 487)
        for row in range(0, 9):
            painter.drawLine(100, 100 + row * 41 + row * 2, 487, 100 + row * 41 + row * 2)

    def keyPressEvent(self, event):
        # IF SPACE IS PRESSED AFTER A BLANK-LABEL IS CLICKED
        if event.key() == Qt.Key_Space:
            # SEARCH FOR THE BLANK-LABEL WE NEED TO DELETE
            for bl in blank_labels:
                if bl.delete:
                    # FIND THE (I,J) LABEL TO SHOW ON TOP OF THE CURRENT BLANK-LABEL
                    for l in labels:
                        if l.i == bl.i and l.j == bl.j:
                            ss.grid[bl.i][bl.j] = 0
                            l.show()
                    bl.delete = False
        # PRESS F TO FINISH THE GAME AND PLACE YOUR LAST ANSWER
        # FOR THE LAST LABEL WE DON T HAVE ANY REMAINING LABELS TO DRAW
        # WE MUST SEARCH THE ONLY NON HIDDEN LABEL AND PREDICT ITS VALUE
        elif event.key() == Qt.Key_F:
            # IF ONLY ONE LABEL REMAINS TO DRAW
            if ss.get_solved() == 1:
                for l in labels:
                    if not l.isHidden():
                        place_prediction(l)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(App.exec_())
