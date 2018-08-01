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


def stateUpdate():
    # print('State Update')
    vState = localRobotStMachObj.getVState()
    # print(vState)
    if vState['V1']['state'] == 'zu':
        V1Btn.setChecked(False)
    else:
        V1Btn.setChecked(True)

    if vState['V2']['state'] == 'zu':
        V2Btn.setChecked(False)
    else:
        V2Btn.setChecked(True)

    if vState['V3']['state'] == 'zu':
        V3Btn.setChecked(False)
    else:
        V3Btn.setChecked(True)

    if vState['V4']['state'] == 'zu':
        V4Btn.setChecked(False)
    else:
        V4Btn.setChecked(True)

    if vState['V5']['state'] == 'zu':
        V5Btn.setChecked(False)
    else:
        V5Btn.setChecked(True)

    if vState['V6']['state'] == 'zu':
        V6Btn.setChecked(False)
    else:
        V6Btn.setChecked(True)

    if vState['V7']['state'] == 'zu':
        V7Btn.setChecked(False)
    else:
        V7Btn.setChecked(True)

    if vState["V_Prop"]["state"] == 'an':
        VPropBtn.setChecked(True)
    else:
        VPropBtn.setChecked(False)

    if vState["V_Prop"]["stellgrad"] >= 50:
        VPropBtn.setChecked(True)
    else:
        VPropBtn.setChecked(False)




@QtCore.pyqtSlot()
def on_click():
    print('PyQt5 button click')
    if localRobotStMachObj.isRunning == True:
        localRobotStMachObj.isRunning = False
    else:
        localRobotStMachObj.isRunning = True
    stateUpdate()

@QtCore.pyqtSlot()
def evacSample():
    print('start evacuating sample')
    localRobotStMachObj.setUserCommand('evacSample')
    stateUpdate()

@QtCore.pyqtSlot()
def alleAuf():
    print('alle Ventile auf')
    localRobotStMachObj.setUserCommand('alleAuf')
    stateUpdate()

@QtCore.pyqtSlot()
def AlleZu():
    print('alle Ventile auf')
    localRobotStMachObj.setUserCommand('AlleZu')
    stateUpdate()

@QtCore.pyqtSlot()
def EvakFine():
    print('Evac Fine')
    localRobotStMachObj.setUserCommand('EvakFine')
    stateUpdate()


@QtCore.pyqtSlot()
def DegassEvaporator():
    print('Degass Evaporator')
    localRobotStMachObj.setUserCommand('DegassEvaporator')
    stateUpdate()


@QtCore.pyqtSlot()
def V1():
    localRobotStMachObj.setUserCommand('V1')
    localRobotStMachObj.getVState()
    stateUpdate()


@QtCore.pyqtSlot()
def V2():
    localRobotStMachObj.setUserCommand('V2')
    stateUpdate()


@QtCore.pyqtSlot()
def V3():
    localRobotStMachObj.setUserCommand('V3')
    stateUpdate()


@QtCore.pyqtSlot()
def V4():
    localRobotStMachObj.setUserCommand('V4')
    stateUpdate()


@QtCore.pyqtSlot()
def V5():
    localRobotStMachObj.setUserCommand('V5')
    stateUpdate()


@QtCore.pyqtSlot()
def V6():
    localRobotStMachObj.setUserCommand('V6')
    stateUpdate()


@QtCore.pyqtSlot()
def V7():
    localRobotStMachObj.setUserCommand('V7')
    stateUpdate()

@QtCore.pyqtSlot()
def VProp():
    localRobotStMachObj.setUserCommand('VProp')
    stateUpdate()


@QtCore.pyqtSlot()
def VPropStellgrad():
    localRobotStMachObj.setUserCommand('VPropStellgrad')
    stateUpdate()


btn = QtGui.QPushButton('start control')
btn.setToolTip('This is an example button')
l.addWidget(btn)
btn.clicked.connect(on_click)

evacBtn = QtGui.QPushButton('evac Sample')
l.addWidget(evacBtn)
evacBtn.clicked.connect(evacSample)

EvakFineBtn = QtGui.QPushButton('Evac Slow')
l.addWidget(EvakFineBtn)
EvakFineBtn.clicked.connect(EvakFine)

alleAufBtn = QtGui.QPushButton('All Valves Open')
l.addWidget(alleAufBtn)
alleAufBtn.clicked.connect(alleAuf)

AlleZuBtn = QtGui.QPushButton('Close all Valves')
l.addWidget(AlleZuBtn)
AlleZuBtn.clicked.connect(AlleZu)

DegassEvaporatorBtn = QtGui.QPushButton('Degass Evaporator')
l.addWidget(DegassEvaporatorBtn)
DegassEvaporatorBtn.clicked.connect(DegassEvaporator)

V1Btn = QtGui.QPushButton('V1')
l.addWidget(V1Btn)
V1Btn.clicked.connect(V1)
V1Btn.setCheckable(True)

V2Btn = QtGui.QPushButton('V2')
l.addWidget(V2Btn)
V2Btn.clicked.connect(V2)
V2Btn.setCheckable(True)

V3Btn = QtGui.QPushButton('V3')
l.addWidget(V3Btn)
V3Btn.clicked.connect(V3)
V3Btn.setCheckable(True)

V4Btn = QtGui.QPushButton('V4')
l.addWidget(V4Btn)
V4Btn.clicked.connect(V4)
V4Btn.setCheckable(True)

V5Btn = QtGui.QPushButton('V5')
l.addWidget(V5Btn)
V5Btn.clicked.connect(V5)
V5Btn.setCheckable(True)

V6Btn = QtGui.QPushButton('V6')
l.addWidget(V6Btn)
V6Btn.clicked.connect(V6)
V6Btn.setCheckable(True)

V7Btn = QtGui.QPushButton('V7')
l.addWidget(V7Btn)
V7Btn.clicked.connect(V7)
V7Btn.setCheckable(True)

VPropBtn = QtGui.QPushButton('VProp On/Off')
l.addWidget(VPropBtn)
VPropBtn.clicked.connect(VProp)
VPropBtn.setCheckable(True)

VPropStellgradBtn = QtGui.QPushButton('VProp Stellgrad')
l.addWidget(VPropStellgradBtn)
VPropStellgradBtn.clicked.connect(VPropStellgrad)
VPropStellgradBtn.setCheckable(True)


text = QtGui.QLineEdit('enter text')
l.addWidget(text)

listw = QtGui.QListWidget()
l.addWidget(listw)
mw.show()

## Create an empty plot curve to be filled later, set its pen
pw.addLegend()
p1 = pw.plot(name="Pressure Sample")
p2 = pw.plot(name="Pressure Manifold")

pw.setLabel('left', 'Value', units='mbar')
pw.setLabel('bottom', 'Time', units='s')


# pw.setXRange(0, 2)

# pw.setYRange(0, 1e-10)


def updateData():
    # Guilogger.info('try Update: p1')
    p1array = localRobotStMachObj.MesskarteObj.getp1ProbeArray()
    p2array = localRobotStMachObj.MesskarteObj.getp2ManifoldArray()
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
    # print("maxPressure1",maxPressure1)
    # if maxPressure1 >= maxPressure2:
    #     pw.setYRange(0, maxPressure1)
    # else:
    #     pw.setYRange(0, maxPressure2)


def UpdateStateMachine():
    Guilogger.debug('trying to update machine')
    localRobotStMachObj.tock()


## Start a timer to rapidly update the plot in pw


t = QtCore.QTimer()
t.timeout.connect(updateData)
t.start(16)  # in msec, 16 entsprechen 60 Hz



timerStatemachine = QtCore.QTimer()
timerStatemachine.timeout.connect(UpdateStateMachine)
## Statemachinetimer muss deutlich schneller sein als der Geräte/Regeltakt, sonst wird Messen nicht ausgelöst
timerStatemachine.start(1)  # in msec

# Timer zum Update der Knöpfe
buttonTimer = QtCore.QTimer()
buttonTimer.timeout.connect(stateUpdate)
buttonTimer.start(500)  # in msec, 16 entsprechen 60 Hz

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
