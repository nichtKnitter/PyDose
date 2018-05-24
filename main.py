import sys

import nidaqmx
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from nidaqmx.constants import (LineGrouping)

print("imported")


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(100, 70)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        with nidaqmx.Task() as task:
            # task.ai_channels.add_ai_voltage_chan("Dev1/ai0","P1",min_val=-10,max_val=10) #,terminal_config=nidaqmx.TerminalConfiguration.RSE,m
            mwchan = task.ai_channels.add_ai_voltage_chan("Dev1/ai0",
                                                          terminal_config=nidaqmx.constants.TerminalConfiguration.RSE,
                                                          min_val=-1, max_val=10)
            bla = task.read()
            print(bla)
            # task.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
