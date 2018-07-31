# -*- coding: utf-8 -*-
"""
Demonstrates use of PlotWidget class. This is little more than a
GraphicsView with a PlotItem placed in its center.
"""

# import time
import logging

import AblaufStatemachine
# import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

# from PyQt5.QtCore import pyqtSlot
# from pyqtgraph.Qt.QtCore import pyqtSlot


logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
Guilogger = logging.getLogger('guilogger')
Guilogger.setLevel(logging.INFO)
# Create the Handler for logging data to a file
logger_handler = logging.FileHandler('python_logging.log')
logger_handler.setLevel(logging.INFO)
# Add the Handler to the Logger
Guilogger.addHandler(logger_handler)
Guilogger.disabled = True
Guilogger.info('Completed configuring logger()!')

# import Messkarte

localRobotStMachObj = AblaufStatemachine.robotStateMachine(
    activeOnStart=False)  # achtung! hier wird batman gleich wieder zerstört

# QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])

# amin window
mw = QtGui.QMainWindow()
mw.setWindowTitle('pyqtgraph example: PlotWidget')
mw.resize(800, 800)

# central widget
cw = QtGui.QWidget()
mw.setCentralWidget(cw)
l = QtGui.QVBoxLayout()
cw.setLayout(l)

pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
l.addWidget(pw)


@QtCore.pyqtSlot()
def on_click():
    print('PyQt5 button click')
    if localRobotStMachObj.isRunning == True:
        localRobotStMachObj.isRunning = False
    else:
        localRobotStMachObj.isRunning = True


@QtCore.pyqtSlot()
def evacSample():
    print('start evacuating sample')
    localRobotStMachObj.MesskarteObj.Ventile_schalten_ges(localRobotStMachObj.MesskarteObj.vStateSollProbeEvakGrob)


@QtCore.pyqtSlot()
def alleAuf():
    print('alle Ventile auf')
    localRobotStMachObj.MesskarteObj.Ventile_schalten_ges(localRobotStMachObj.MesskarteObj.vStateSollAlleAuf)


btn = QtGui.QPushButton('start control')
btn.setToolTip('This is an example button')
l.addWidget(btn)
btn.clicked.connect(on_click)

evacBtn = QtGui.QPushButton('evac Sample')
l.addWidget(evacBtn)
evacBtn.clicked.connect(evacSample)

alleAufBtn = QtGui.QPushButton('All Valves Open')
l.addWidget(alleAufBtn)
alleAufBtn.clicked.connect(alleAuf)

text = QtGui.QLineEdit('enter text')
l.addWidget(text)

listw = QtGui.QListWidget()
l.addWidget(listw)
mw.show()

## Create an empty plot curve to be filled later, set its pen
p1 = pw.plot()
p2 = pw.plot()

pw.setLabel('left', 'Value', units='V')
pw.setLabel('bottom', 'Time', units='s')


# pw.setXRange(0, 2)

# pw.setYRange(0, 1e-10)


def updateData():
    # p1.setData(y=yd, x=xd)
    # Guilogger.info('try Update: p1')
    p2array = localRobotStMachObj.MesskarteObj.getp2ManifoldArray()
    # Guilogger.info(str(p1array))
    # Guilogger.info("p1 zugriff erfolgreich")

    # Guilogger.info("try p2")
    p1array = localRobotStMachObj.MesskarteObj.getp1ProbeArray()
    # Guilogger.info(str(p2array))
    # Guilogger.info(" p2 zugriff erfolgreich")

    # Guilogger.info("try p2 array")
    timearray = localRobotStMachObj.MesskarteObj.getTimearray()
    # Guilogger.info(str(timearray))
    # Guilogger.info("timezugriff erfolgreich")

    # Guilogger.info ('trying to update plot')
    p1.setData(x=timearray, y=p1array, pen=pg.mkPen('b', width=1))
    p2.setData(x=timearray, y=p2array, pen=pg.mkPen('r', width=1))
    Guilogger.info('Plot geupdatet')

    maxPressure1 = max(p1array)
    maxPressure2 = max(p2array)
    # max(maxPressure1,maxPressure2)
    # print("maxPressure",maxPressure)
    # pw.setYRange(0, maxPressure)


def UpdateStateMachine():
    Guilogger.debug('trying to update machine')
    localRobotStMachObj.tock()


## Start a timer to rapidly update the plot in pw


t = QtCore.QTimer()
t.timeout.connect(updateData)
t.start(100)
# updateData()


timerStatemachine = QtCore.QTimer()
timerStatemachine.timeout.connect(UpdateStateMachine)
timerStatemachine.start(100)

## Multiple parameterized plots--we can autogenerate averages for these.
# for i in range(0, 5):
#     for j in range(0, 3):
#         yd, xd = rand(10000)
#         pw2.plot(y=yd * (j + 1), x=xd, params={'iter': i, 'val': j})

## Test large numbers
# curve = pw3.plot(np.random.normal(size=100) * 1e0, clickable=True)
# curve.curve.setClickable(True)
# curve.setPen('w')  ## white pen
# curve.setShadowPen(pg.mkPen((70, 70, 30), width=6, cosmetic=True))


# def clicked():
#     print("curve clicked")


# curve.sigClicked.connect(clicked)

# lr = pg.LinearRegionItem([1, 30], bounds=[0, 100], movable=True)
# pw3.addItem(lr)
# line = pg.InfiniteLine(angle=90, movable=True)
# pw3.addItem(line)
# line.setBounds([0, 200])

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
