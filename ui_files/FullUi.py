# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FullUi.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QWidget)

from modules.DragDropLineEdit import DragDropLineEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(921, 665)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 0, 3, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.light_dark_switch = QPushButton(self.widget)
        self.light_dark_switch.setObjectName(u"light_dark_switch")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.light_dark_switch.sizePolicy().hasHeightForWidth())
        self.light_dark_switch.setSizePolicy(sizePolicy)
        self.light_dark_switch.setCheckable(True)
        self.light_dark_switch.setChecked(True)

        self.horizontalLayout_3.addWidget(self.light_dark_switch)

        self.light_dark_color_selector = QComboBox(self.widget)
        self.light_dark_color_selector.setObjectName(u"light_dark_color_selector")

        self.horizontalLayout_3.addWidget(self.light_dark_color_selector)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.json_load_enable = QCheckBox(self.widget)
        self.json_load_enable.setObjectName(u"json_load_enable")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.json_load_enable)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.json_load = DragDropLineEdit(self.widget)
        self.json_load.setObjectName(u"json_load")
        self.json_load.setEnabled(False)

        self.horizontalLayout.addWidget(self.json_load)

        self.json_load_select = QPushButton(self.widget)
        self.json_load_select.setObjectName(u"json_load_select")
        self.json_load_select.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.json_load_select.sizePolicy().hasHeightForWidth())
        self.json_load_select.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.json_load_select)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        self.checkBox = QCheckBox(self.widget)
        self.checkBox.setObjectName(u"checkBox")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.checkBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.json_folder_input = DragDropLineEdit(self.widget)
        self.json_folder_input.setObjectName(u"json_folder_input")
        self.json_folder_input.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.json_folder_input)

        self.json_name_input = QLineEdit(self.widget)
        self.json_name_input.setObjectName(u"json_name_input")
        self.json_name_input.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.json_name_input)

        self.json_folder_select = QPushButton(self.widget)
        self.json_folder_select.setObjectName(u"json_folder_select")
        self.json_folder_select.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.json_folder_select.sizePolicy().hasHeightForWidth())
        self.json_folder_select.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.json_folder_select)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.start_training = QPushButton(self.widget)
        self.start_training.setObjectName(u"start_training")

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.start_training)


        self.gridLayout.addWidget(self.widget, 1, 2, 1, 3)

        self.gridLayout.setRowStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Change Theme", None))
        self.light_dark_switch.setText("")
        self.json_load_enable.setText(QCoreApplication.translate("MainWindow", u"Load Json File", None))
        self.json_load.setPlaceholderText(QCoreApplication.translate("MainWindow", u"configuration json file", None))
        self.json_load_select.setText("")
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Save Json File", None))
        self.json_folder_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"save location", None))
        self.json_name_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"save name", None))
        self.json_folder_select.setText("")
        self.start_training.setText(QCoreApplication.translate("MainWindow", u"Start Training", None))
    # retranslateUi

