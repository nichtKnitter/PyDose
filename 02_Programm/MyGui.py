# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiv002.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1396, 936)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.graphicsViewForPlotWidget = PlotWidget(self.groupBox_4)
        self.graphicsViewForPlotWidget.setObjectName("graphicsViewForPlotWidget")
        self.gridLayout_2.addWidget(self.graphicsViewForPlotWidget, 0, 0, 1, 1)
        self.graphicsViewForPlotWidget.raise_()
        self.gridLayout.addWidget(self.groupBox_4, 1, 2, 8, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.startBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayout_4.addWidget(self.startBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.PressureSetpointSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.PressureSetpointSpinBox.setObjectName("PressureSetpointSpinBox")
        self.horizontalLayout.addWidget(self.PressureSetpointSpinBox)
        self.setPressureSetpointBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.setPressureSetpointBtn.setObjectName("setPressureSetpointBtn")
        self.horizontalLayout.addWidget(self.setPressureSetpointBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.horizontalLayout_2.addWidget(self.doubleSpinBox_2)
        self.pushButton_9 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_2.addWidget(self.pushButton_9)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.vPropSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.vPropSpinBox.setObjectName("vPropSpinBox")
        self.horizontalLayout_3.addWidget(self.vPropSpinBox)
        self.VPropStellgradBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.VPropStellgradBtn.setObjectName("VPropStellgradBtn")
        self.horizontalLayout_3.addWidget(self.VPropStellgradBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_13 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_13.setObjectName("pushButton_13")
        self.verticalLayout_2.addWidget(self.pushButton_13)
        self.pushButton_16 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_16.setObjectName("pushButton_16")
        self.verticalLayout_2.addWidget(self.pushButton_16)
        self.pushButton_14 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_14.setObjectName("pushButton_14")
        self.verticalLayout_2.addWidget(self.pushButton_14)
        self.pushButton_15 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_15.setObjectName("pushButton_15")
        self.verticalLayout_2.addWidget(self.pushButton_15)
        self.verticalLayout_3.addWidget(self.groupBox_5)
        self.gridLayout.addWidget(self.groupBox_2, 6, 0, 3, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_5.addWidget(self.textBrowser)
        self.gridLayout.addWidget(self.groupBox_6, 8, 1, 1, 1)
        self.groupBoxSchema = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxSchema.sizePolicy().hasHeightForWidth())
        self.groupBoxSchema.setSizePolicy(sizePolicy)
        self.groupBoxSchema.setMinimumSize(QtCore.QSize(680, 429))
        self.groupBoxSchema.setMaximumSize(QtCore.QSize(680, 429))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBoxSchema.setFont(font)
        self.groupBoxSchema.setAutoFillBackground(False)
        self.groupBoxSchema.setStyleSheet("#groupBoxSchema{\n"
"background-image: url(:/newPrefix/image.png);\n"
"}")
        self.groupBoxSchema.setObjectName("groupBoxSchema")
        self.V3Btn = QtWidgets.QPushButton(self.groupBoxSchema)
        self.V3Btn.setEnabled(True)
        self.V3Btn.setGeometry(QtCore.QRect(170, 40, 31, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V3Btn.sizePolicy().hasHeightForWidth())
        self.V3Btn.setSizePolicy(sizePolicy)
        self.V3Btn.setCheckable(True)
        self.V3Btn.setObjectName("V3Btn")
        self.V1Btn = QtWidgets.QPushButton(self.groupBoxSchema)
        self.V1Btn.setEnabled(True)
        self.V1Btn.setGeometry(QtCore.QRect(290, 240, 31, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V1Btn.sizePolicy().hasHeightForWidth())
        self.V1Btn.setSizePolicy(sizePolicy)
        self.V1Btn.setAutoFillBackground(True)
        self.V1Btn.setCheckable(True)
        self.V1Btn.setChecked(False)
        self.V1Btn.setObjectName("V1Btn")
        self.V2Btn = QtWidgets.QPushButton(self.groupBoxSchema)
        self.V2Btn.setEnabled(True)
        self.V2Btn.setGeometry(QtCore.QRect(170, 180, 31, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V2Btn.sizePolicy().hasHeightForWidth())
        self.V2Btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.V2Btn.setFont(font)
        self.V2Btn.setCheckable(True)
        self.V2Btn.setObjectName("V2Btn")
        self.V4Btn = QtWidgets.QPushButton(self.groupBoxSchema)
        self.V4Btn.setEnabled(True)
        self.V4Btn.setGeometry(QtCore.QRect(290, 30, 31, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V4Btn.sizePolicy().hasHeightForWidth())
        self.V4Btn.setSizePolicy(sizePolicy)
        self.V4Btn.setCheckable(True)
        self.V4Btn.setObjectName("V4Btn")
        self.V6Btn = QtWidgets.QPushButton(self.groupBoxSchema)
        self.V6Btn.setEnabled(True)
        self.V6Btn.setGeometry(QtCore.QRect(400, 70, 31, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V6Btn.sizePolicy().hasHeightForWidth())
        self.V6Btn.setSizePolicy(sizePolicy)
        self.V6Btn.setCheckable(True)
        self.V6Btn.setObjectName("V6Btn")
        self.label_2 = QtWidgets.QLabel(self.groupBoxSchema)
        self.label_2.setGeometry(QtCore.QRect(440, 50, 81, 10))
        self.label_2.setObjectName("label_2")
        self.V5Btn = QtWidgets.QPushButton(self.groupBoxSchema)
        self.V5Btn.setEnabled(True)
        self.V5Btn.setGeometry(QtCore.QRect(290, 110, 31, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V5Btn.sizePolicy().hasHeightForWidth())
        self.V5Btn.setSizePolicy(sizePolicy)
        self.V5Btn.setCheckable(True)
        self.V5Btn.setObjectName("V5Btn")
        self.V7Btn = QtWidgets.QPushButton(self.groupBoxSchema)
        self.V7Btn.setEnabled(True)
        self.V7Btn.setGeometry(QtCore.QRect(410, 180, 31, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V7Btn.sizePolicy().hasHeightForWidth())
        self.V7Btn.setSizePolicy(sizePolicy)
        self.V7Btn.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"alternate-background-color: rgb(255, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.V7Btn.setCheckable(True)
        self.V7Btn.setObjectName("V7Btn")
        self.VPropBtn = QtWidgets.QPushButton(self.groupBoxSchema)
        self.VPropBtn.setEnabled(True)
        self.VPropBtn.setGeometry(QtCore.QRect(230, 110, 41, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VPropBtn.sizePolicy().hasHeightForWidth())
        self.VPropBtn.setSizePolicy(sizePolicy)
        self.VPropBtn.setCheckable(True)
        self.VPropBtn.setObjectName("VPropBtn")
        self.label_7 = QtWidgets.QLabel(self.groupBoxSchema)
        self.label_7.setGeometry(QtCore.QRect(350, 40, 81, 30))
        self.label_7.setObjectName("label_7")
        self.V3Btn.raise_()
        self.V1Btn.raise_()
        self.V2Btn.raise_()
        self.V4Btn.raise_()
        self.V6Btn.raise_()
        self.label_2.raise_()
        self.V5Btn.raise_()
        self.V7Btn.raise_()
        self.VPropBtn.raise_()
        self.label_7.raise_()
        self.gridLayout.addWidget(self.groupBoxSchema, 1, 0, 3, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.AlleZuBtn = QtWidgets.QPushButton(self.groupBox_3)
        self.AlleZuBtn.setObjectName("AlleZuBtn")
        self.gridLayout_3.addWidget(self.AlleZuBtn, 5, 0, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_3.addWidget(self.pushButton_10, 1, 0, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout_3.addWidget(self.pushButton_11, 2, 0, 1, 1)
        self.EvakFineBtn = QtWidgets.QPushButton(self.groupBox_3)
        self.EvakFineBtn.setObjectName("EvakFineBtn")
        self.gridLayout_3.addWidget(self.EvakFineBtn, 4, 0, 1, 1)
        self.DegassEvaporatorBtn = QtWidgets.QPushButton(self.groupBox_3)
        self.DegassEvaporatorBtn.setObjectName("DegassEvaporatorBtn")
        self.gridLayout_3.addWidget(self.DegassEvaporatorBtn, 3, 0, 1, 1)
        self.evacBtn = QtWidgets.QPushButton(self.groupBox_3)
        self.evacBtn.setObjectName("evacBtn")
        self.gridLayout_3.addWidget(self.evacBtn, 0, 0, 1, 1)
        self.blabtn = QtWidgets.QPushButton(self.groupBox_3)
        self.blabtn.setObjectName("blabtn")
        self.gridLayout_3.addWidget(self.blabtn, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 6, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1396, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Live Plot"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Automatic Control"))
        self.label_4.setText(_translate("MainWindow", "Automode:"))
        self.startBtn.setText(_translate("MainWindow", "Start Dosing"))
        self.label_5.setText(_translate("MainWindow", "Pressure Setpoint:"))
        self.setPressureSetpointBtn.setText(_translate("MainWindow", "send"))
        self.label_3.setText(_translate("MainWindow", "Temperature Setpoint"))
        self.pushButton_9.setText(_translate("MainWindow", "send"))
        self.label_6.setText(_translate("MainWindow", "Proportional Valve %"))
        self.VPropStellgradBtn.setText(_translate("MainWindow", "send"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Measurement"))
        self.pushButton_13.setText(_translate("MainWindow", "New Measurement config"))
        self.pushButton_16.setText(_translate("MainWindow", "New Measurement config"))
        self.pushButton_14.setText(_translate("MainWindow", "Load Measurement config"))
        self.pushButton_15.setText(_translate("MainWindow", "Start Measurement"))
        self.groupBox_6.setTitle(_translate("MainWindow", "GroupBox"))
        self.groupBoxSchema.setTitle(_translate("MainWindow", "Scheme"))
        self.V3Btn.setText(_translate("MainWindow", "V3"))
        self.V1Btn.setText(_translate("MainWindow", "V1"))
        self.V2Btn.setText(_translate("MainWindow", "V2"))
        self.V4Btn.setText(_translate("MainWindow", "V4"))
        self.V6Btn.setText(_translate("MainWindow", "V6"))
        self.label_2.setText(_translate("MainWindow", "P Sample mbar"))
        self.V5Btn.setText(_translate("MainWindow", "V5"))
        self.V7Btn.setText(_translate("MainWindow", "V7"))
        self.VPropBtn.setText(_translate("MainWindow", "VProp"))
        self.label_7.setText(_translate("MainWindow", "P Manifold mbar"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Manual Control"))
        self.AlleZuBtn.setText(_translate("MainWindow", "Close All"))
        self.pushButton_10.setText(_translate("MainWindow", "Evac. Manifold"))
        self.pushButton_11.setText(_translate("MainWindow", "Ventilate"))
        self.EvakFineBtn.setText(_translate("MainWindow", "Evac. Slow"))
        self.DegassEvaporatorBtn.setText(_translate("MainWindow", "Degass Evap."))
        self.evacBtn.setText(_translate("MainWindow", "Evac. Sample"))
        self.blabtn.setText(_translate("MainWindow", "blabla"))

from pyqtgraph import PlotWidget
import schema_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

