# -*- coding: utf-8 -*-
"""
Demonstrates use of PlotWidget class. This is little more than a
GraphicsView with a PlotItem placed in its center.
"""

# import time
import logging

import AblaufStatemachine
# import numpy as np
import pyqtgraph as pyqtgraph
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets




logging.basicConfig(level=logging.INFO)
# Set transitions' log level to INFO; DEBUG messages will be omitted
Guilogger = logging.getLogger('guilogger')
Guilogger.setLevel(logging.INFO)
# Create the Handler for logging data to a file
logger_handler = logging.FileHandler('python_logging.log')
logger_handler.setLevel(logging.INFO)
# Add the Handler to the Logger
Guilogger.addHandler(logger_handler)
Guilogger.disabled = False
Guilogger.info('Completed configuring logger()!')

# import Messkarte

import sys
from PyQt5.QtWidgets import QApplication


class Example(QtGui.QMainWindow):
    localRobotStMachObj = AblaufStatemachine.robotStateMachine(
        activeOnStart=False)  # achtung! hier wird batman gleich wieder zerstört

    def __init__(self):
        super().__init__()
        self.initUI()
        self.vState = self.localRobotStMachObj.getVState()
        Guilogger.info("Init: VState  ")

        self.t = QtCore.QTimer()
        self.t.timeout.connect(self.updateData)

        self.timerStatemachine = QtCore.QTimer()
        self.timerStatemachine.timeout.connect(self.UpdateStateMachine)

        # Timer zum Update der Knöpfe
        self.buttonTimer = QtCore.QTimer()
        self.buttonTimer.timeout.connect(self.stateUpdate)

        Guilogger.debug("timer gestartet")
        self.t.start(16)  # in msec, 16 entsprechen 60 Hz
        ## Statemachinetimer muss deutlich schneller sein als der Geräte/Regeltakt, sonst wird Messen nicht ausgelöst
        self.timerStatemachine.start(1)  # in msec
        self.buttonTimer.start(100)  # in msec, 16 entsprechen 60 Hz

    def initUI(self):
        self.statusBar().showMessage('Ready')

        self.setGeometry(300, 300, 250, 150)
        self.resize(1600, 800)
        self.setWindowTitle('Statusbar')

        # central widget
        self.cw = QtGui.QWidget()  # central window?
        self.setCentralWidget(self.cw)
        self.l = QtGui.QVBoxLayout()
        self.cw.setLayout(self.l)

        self.pw = pyqtgraph.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
        self.l.addWidget(self.pw)

        self.initButtons()

        ## Create an empty plot curve to be filled later, set its pen
        self.pw.addLegend()
        self.p1 = self.pw.plot(name="Pressure Mainifold")
        self.p2 = self.pw.plot(name="Pressure Sample")

        self.pw.setLabel('left', 'Value', units='mbar')
        self.pw.setLabel('bottom', 'Time', units='s')

        self.show()

    def initButtons(self):



        self.startBtn = QtGui.QPushButton('Start Control')
        self.startBtn.setToolTip('This is an example button')
        self.l.addWidget(self.startBtn)
        self.startBtn.clicked.connect(self.startDosing)
        self.startBtn.setCheckable(True)

        self.evacBtn = QtGui.QPushButton('evac Sample')
        self.l.addWidget(self.evacBtn)
        self.evacBtn.clicked.connect(self.evacSample)

        self.EvakFineBtn = QtGui.QPushButton('Evac Slow')
        self.l.addWidget(self.EvakFineBtn)
        self.EvakFineBtn.clicked.connect(self.EvakFine)

        self.alleAufBtn = QtGui.QPushButton('All Valves Open')
        self.l.addWidget(self.alleAufBtn)
        self.alleAufBtn.clicked.connect(self.alleAuf)

        self.AlleZuBtn = QtGui.QPushButton('Close all Valves')
        self.l.addWidget(self.AlleZuBtn)
        self.AlleZuBtn.clicked.connect(self.AlleZu)

        self.DegassEvaporatorBtn = QtGui.QPushButton('Degass Evaporator')
        self.l.addWidget(self.DegassEvaporatorBtn)
        self.DegassEvaporatorBtn.clicked.connect(self.DegassEvaporator)

        self.V1Btn = QtGui.QPushButton('V1')
        self.l.addWidget(self.V1Btn)
        self.V1Btn.clicked.connect(self.V1)
        self.V1Btn.setCheckable(True)

        self.V2Btn = QtGui.QPushButton('V2')
        self.l.addWidget(self.V2Btn)
        self.V2Btn.clicked.connect(self.V2)
        self.V2Btn.setCheckable(True)

        self.V3Btn = QtGui.QPushButton('V3')
        self.l.addWidget(self.V3Btn)
        self.V3Btn.clicked.connect(self.V3)
        self.V3Btn.setCheckable(True)

        self.V4Btn = QtGui.QPushButton('V4')
        self.l.addWidget(self.V4Btn)
        self.V4Btn.clicked.connect(self.V4)
        self.V4Btn.setCheckable(True)

        self.V5Btn = QtGui.QPushButton('V5')
        self.l.addWidget(self.V5Btn)
        self.V5Btn.clicked.connect(self.V5)
        self.V5Btn.setCheckable(True)

        self.V6Btn = QtGui.QPushButton('V6')
        self.l.addWidget(self.V6Btn)
        self.V6Btn.clicked.connect(self.V6)
        self.V6Btn.setCheckable(True)

        self.V7Btn = QtGui.QPushButton('V7')
        self.l.addWidget(self.V7Btn)
        self.V7Btn.clicked.connect(self.V7)
        self.V7Btn.setCheckable(True)

        self.VPropBtn = QtGui.QPushButton('VProp On/Off')
        self.l.addWidget(self.VPropBtn)
        self.VPropBtn.clicked.connect(self.VProp)
        self.VPropBtn.setCheckable(True)

        self.VPropStellgradBtn = QtGui.QPushButton('VProp Stellgrad')
        self.l.addWidget(self.VPropStellgradBtn)
        # self.VPropStellgradBtn.clicked.connect(self.VPropStellgrad)
        self.VPropStellgradBtn.setCheckable(True)

    def stateUpdate(self):
        # print('State Update')
        self.vState = self.localRobotStMachObj.getVState()
        Guilogger.debug(self.vState)
        Guilogger.debug("state Update: is Running =")
        Guilogger.debug(str(self.localRobotStMachObj.getIsRunning()))

        message = "Automatic Control: " + str(self.localRobotStMachObj.getIsRunning()) + "\t\t\tActual Mode: " + \
                  self.vState['State']['Name']
        self.statusBar().showMessage(message)

        if self.localRobotStMachObj.getIsRunning() is True:
            self.startBtn.setChecked(True)
        else:
            self.startBtn.setChecked(False)

        if self.vState['V1']['state'] == 'zu':
            self.V1Btn.setChecked(False)
        else:
            self.V1Btn.setChecked(True)

        if self.vState['V2']['state'] == 'zu':
            self.V2Btn.setChecked(False)
        else:
            self.V2Btn.setChecked(True)

        if self.vState['V3']['state'] == 'zu':
            self.V3Btn.setChecked(False)
        else:
            self.V3Btn.setChecked(True)

        if self.vState['V4']['state'] == 'zu':
            self.V4Btn.setChecked(False)
        else:
            self.V4Btn.setChecked(True)

        if self.vState['V5']['state'] == 'zu':
            self.V5Btn.setChecked(False)
        else:
            self.V5Btn.setChecked(True)

        if self.vState['V6']['state'] == 'zu':
            self.V6Btn.setChecked(False)
        else:
            self.V6Btn.setChecked(True)

        if self.vState['V7']['state'] == 'zu':
            self.V7Btn.setChecked(False)
        else:
            self.V7Btn.setChecked(True)

        if self.vState["V_Prop"]["state"] == 'an':
            self.VPropBtn.setChecked(True)
        else:
            self.VPropBtn.setChecked(False)

        if self.vState["V_Prop"]["stellgrad"] >= 50:
            self.VPropStellgradBtn.setChecked(True)
        else:
            self.VPropStellgradBtn.setChecked(False)

    @QtCore.pyqtSlot()
    def startDosing(self):
        Guilogger.info('Dosing gestertet')
        Guilogger.info(self.localRobotStMachObj.getIsRunning())
        if self.localRobotStMachObj.getIsRunning() is True:
            self.localRobotStMachObj.setIsRunning(False)
            Guilogger.info("Dosing gestoppt")
        else:
            self.localRobotStMachObj.setIsRunning(True)
            Guilogger.info("Dosing aktiviert")
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def evacSample(self):
        print('start evacuating sample')
        self.localRobotStMachObj.setUserCommand('evacSample')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def alleAuf(self):
        print('alle Ventile auf')
        self.localRobotStMachObj.setUserCommand('alleAuf')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def AlleZu(self):
        print('alle Ventile auf')
        self.localRobotStMachObj.setUserCommand('AlleZu')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def EvakFine(self):
        print('Evac Fine')
        self.localRobotStMachObj.setUserCommand('EvakFine')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def DegassEvaporator(self):
        print('Degass Evaporator')
        self.localRobotStMachObj.setUserCommand('DegassEvaporator')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def V1(self):
        self.localRobotStMachObj.setUserCommand('V1')
        self.localRobotStMachObj.getVState()
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def V2(self):
        self.localRobotStMachObj.setUserCommand('V2')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def V3(self):
        self.localRobotStMachObj.setUserCommand('V3')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def V4(self):
        self.localRobotStMachObj.setUserCommand('V4')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def V5(self):
        self.localRobotStMachObj.setUserCommand('V5')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def V6(self):
        self.localRobotStMachObj.setUserCommand('V6')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def V7(self):
        self.localRobotStMachObj.setUserCommand('V7')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def VProp(self):
        self.localRobotStMachObj.setUserCommand('VProp')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def VPropStellgrad(self):
        self.localRobotStMachObj.setUserCommand('VPropStellgrad')
        self.stateUpdate()

    def updateData(self):
        Guilogger.debug("updating Plotdata")
        self.p1array = self.localRobotStMachObj.MesskarteObj.getp1ManifoldArray()
        Guilogger.debug(str(self.p1array))
        self.p2array = self.localRobotStMachObj.MesskarteObj.getp2ProbeArray()
        Guilogger.debug(str(self.p2array))
        self.timearray = self.localRobotStMachObj.MesskarteObj.getTimearray()
        Guilogger.debug(str(self.timearray))
        self.p1.setData(x=self.timearray, y=self.p1array, pen=pyqtgraph.mkPen('b', width=1))
        self.p2.setData(x=self.timearray, y=self.p2array, pen=pyqtgraph.mkPen('r', width=1))
        # Guilogger.info('Plot geupdatet')

        self.maxPressure1 = max(self.p1array)
        self.maxPressure2 = max(self.p2array)

    def UpdateStateMachine(self):
        # Guilogger.debug('trying to update machine')
        self.localRobotStMachObj.tock()

    ## Start a timer to rapidly update the plot in pw


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
