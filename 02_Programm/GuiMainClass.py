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
# import Ui_MainWindow as Ui_MainAuto
from MyGui import Ui_MainWindow
from pyqtgraph.Qt import QtGui, QtCore

# from PyQt5 import QtCore, QtGui, QtWidgets


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


class Example(QtGui.QMainWindow, Ui_MainWindow):
    localRobotStMachObj = AblaufStatemachine.robotStateMachine(
        activeOnStart=False)  # achtung! hier wird batman gleich wieder zerstört

    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        self.setupUi(self)

        self.initUIafterAuto()
        # self.vState = self.localRobotStMachObj.getVState()
        # Guilogger.info("Init: VState  ")
        #
        self.t = QtCore.QTimer()
        self.t.timeout.connect(self.updateData)
        #
        self.timerStatemachine = QtCore.QTimer()
        self.timerStatemachine.timeout.connect(self.UpdateStateMachine)
        #
        # # Timer zum Update der Knöpfe
        self.buttonTimer = QtCore.QTimer()
        self.buttonTimer.timeout.connect(self.stateUpdate)

        Guilogger.debug("timer gestartet")
        self.t.start(16)  # in msec, 16 entsprechen 60 Hz
        # ## Statemachinetimer muss deutlich schneller sein als der Geräte/Regeltakt, sonst wird Messen nicht ausgelöst
        self.timerStatemachine.start(1)  # in msec
        self.buttonTimer.start(16)  # in msec, 16 entsprechen 60 Hz

    def initUIafterAuto(self):
        self.statusBar().showMessage('Ready')
        print(self.centralwidget)

        # self.setWindowTitle('Statusbar')

        print(self.graphicsViewForPlotWidget)

        self.connectButtons()

        ## Create an empty plot curve to be filled later, set its pen
        # self.graphicsViewForPlotWidget = pyqtgraph.PlotWidget(
        #     name='Plot1')  ## giving the plots names allows us to link their axes together
        self.graphicsViewForPlotWidget.addLegend()
        self.p1 = self.graphicsViewForPlotWidget.plot(name="Pressure Mainifold")
        self.p2 = self.graphicsViewForPlotWidget.plot(name="Pressure Sample")
        self.p3 = self.graphicsViewForPlotWidget.plot(name="Setpoint")
        self.graphicsViewForPlotWidget.setRange(yRange=[0, 100], padding=0.01)
        self.graphicsViewForPlotWidget.setDownsampling(ds=5, auto=False, mode='mean')
        #
        self.graphicsViewForPlotWidget.setLabel('left', 'Value', units='mbar')
        self.graphicsViewForPlotWidget.setLabel('bottom', 'Time', units='s')

        # self.graphicsViewForPlotWidget.plot(yRange=[0, 100], maxRange=[0, 120])
        # .setLimits(xRange=[-100, 100], minRange=[0.1, None])

        self.PressureSetpointSpinBox.setValue(self.localRobotStMachObj.MesskarteObj.getSetpoint())


        self.show()

    def connectButtons(self):
        # TODO: Ventile und degass manifold, ....

        # self.alleAufBtn.clicked.connect(self.alleAuf)

        # self.VPropStellgradBtn = QtGui.QPushButton('VProp Stellgrad')
        # self.layoutControlButtons.addWidget(self.VPropStellgradBtn)
        self.VPropStellgradBtn.clicked.connect(self.VPropStellgrad)
        self.VPropStellgradBtn.setCheckable(False)

        self.setPressureSetpointBtn.clicked.connect(self.setPSampleSetpoint)
        self.setPressureSetpointBtn.setCheckable(False)

        self.startBtn.setToolTip('start automatic pressure control')
        self.startBtn.clicked.connect(self.startDosing)
        self.startBtn.setCheckable(True)

        self.evacBtn.clicked.connect(self.evacSample)
        self.evacBtn.setCheckable(True)

        self.DegassEvaporatorBtn.clicked.connect(self.DegassEvaporator)
        self.DegassEvaporatorBtn.setCheckable(True)

        self.EvakFineBtn.clicked.connect(self.EvakFine)
        self.EvakFineBtn.setCheckable(True)

        self.AlleZuBtn.clicked.connect(self.AlleZu)
        #

        self.V1Btn.clicked.connect(self.V1)
        self.V1Btn.setCheckable(True)
        #
        self.V2Btn.clicked.connect(self.V2)
        self.V2Btn.setCheckable(True)
        #
        self.V3Btn.clicked.connect(self.V3)
        self.V3Btn.setCheckable(True)
        #
        self.V4Btn.clicked.connect(self.V4)
        self.V4Btn.setCheckable(True)
        #
        self.V5Btn.clicked.connect(self.V5)
        self.V5Btn.setCheckable(True)
        #
        self.V6Btn.clicked.connect(self.V6)
        self.V6Btn.setCheckable(True)
        #
        self.V7Btn.clicked.connect(self.V7)
        self.V7Btn.setCheckable(True)
        #
        self.VPropBtn.clicked.connect(self.VProp)
        self.VPropBtn.setCheckable(True)
        #


    def stateUpdate(self):

        self.vState = self.localRobotStMachObj.getVState()
        Guilogger.debug(self.vState)
        Guilogger.debug("state Update: is Running =")
        Guilogger.debug(str(self.localRobotStMachObj.getIsRunning()))

        message = "Automatic Control: " + str(self.localRobotStMachObj.getIsRunning()) + "\t\t\tActual Mode: " + \
                  self.vState['State']['Name'] + "\t\t\tStellgrad: " + "{0:0.2f}".format(
            self.localRobotStMachObj.MesskarteObj.lastStellgrad)

        # print(message)
        self.statusBar().showMessage(message)
        if self.localRobotStMachObj.getIsRunning() is True:
            self.startBtn.setChecked(True)
        else:
            self.startBtn.setChecked(False)
        # print('State Update now!!!!!')

        if self.vState["State"]["Name"] == "vStateSollProbeEvakGrob":
            self.evacBtn.setChecked(True)
        else:
            self.evacBtn.setChecked(False)

        if self.vState["State"]["Name"] == "vStateSollDegassEvaporator":
            self.DegassEvaporatorBtn.setChecked(True)
        else:
            self.DegassEvaporatorBtn.setChecked(False)

        if self.vState["State"]["Name"] == "vStateSollEvakFine":
            self.EvakFineBtn.setChecked(True)
        else:
            self.EvakFineBtn.setChecked(False)

        if self.vState["State"]["Name"] == "vStateSollAlleZu":
            self.AlleZuBtn.setChecked(True)
        else:
            self.AlleZuBtn.setChecked(False)

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
        #
        if self.vState["V_Prop"]["state"] == 'an':
            self.VPropBtn.setChecked(True)
        else:
            self.VPropBtn.setChecked(False)
        #


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
        bla = self.vPropSpinBox.value()
        print("neuer Soll Stellgrad", bla)
        self.localRobotStMachObj.PropStellgradSollProzent = bla
        self.localRobotStMachObj.setUserCommand('VPropStellgrad')
        self.stateUpdate()

    @QtCore.pyqtSlot()
    def setPSampleSetpoint(self):
        newSetpoint = self.PressureSetpointSpinBox.value()
        self.localRobotStMachObj.MesskarteObj.setSetpoint(newSetpoint)
        # setSolldruck(newSetpoint)


    def updateData(self):
        Guilogger.debug("updating Plotdata")
        self.p1array = self.localRobotStMachObj.MesskarteObj.getp1ManifoldArray()
        Guilogger.debug(str(self.p1array))
        self.p2array = self.localRobotStMachObj.MesskarteObj.getp2ProbeArray()
        Guilogger.debug(str(self.p2array))
        self.timearray = self.localRobotStMachObj.MesskarteObj.getTimearray()
        Guilogger.debug(str(self.timearray))

        setpointarray = self.localRobotStMachObj.MesskarteObj.setpointarray
        self.p1.setData(x=self.timearray, y=self.p1array, pen=pyqtgraph.mkPen('b', width=1))
        self.p2.setData(x=self.timearray, y=self.p2array, pen=pyqtgraph.mkPen('r', width=1))
        self.p3.setData(x=self.timearray, y=setpointarray, pen=pyqtgraph.mkPen('g', width=1))

        # Guilogger.info('Plot geupdatet')

        self.maxPressure1 = max(self.p1array)
        self.maxPressure2 = max(self.p2array)

    def UpdateStateMachine(self):
        # Guilogger.debug('trying to update machine')
        self.localRobotStMachObj.tock()



if __name__ == '__main__':
    ### original oberfläche
    # app = QApplication(sys.argv)
    # ex = Example()
    # sys.exit(app.exec_())

    ### automatischer code aus MyGuiy.py
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())

    ### Code aus Besipiel
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = Example()  # We set the form to be our ExampleApp (design)
    # form.show()  # Show the form
    app.exec_()  # and execute the app
