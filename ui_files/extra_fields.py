# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'extra_fields.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_extra_fields_ui(object):
    def setupUi(self, extra_fields_ui):
        if not extra_fields_ui.objectName():
            extra_fields_ui.setObjectName(u"extra_fields_ui")
        extra_fields_ui.resize(520, 651)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(extra_fields_ui.sizePolicy().hasHeightForWidth())
        extra_fields_ui.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(extra_fields_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.add_extra_arg_button = QPushButton(extra_fields_ui)
        self.add_extra_arg_button.setObjectName(u"add_extra_arg_button")

        self.horizontalLayout.addWidget(self.add_extra_arg_button)

        self.save_extra_args_button = QPushButton(extra_fields_ui)
        self.save_extra_args_button.setObjectName(u"save_extra_args_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.save_extra_args_button.sizePolicy().hasHeightForWidth())
        self.save_extra_args_button.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.save_extra_args_button)

        self.load_extra_args_button = QPushButton(extra_fields_ui)
        self.load_extra_args_button.setObjectName(u"load_extra_args_button")
        sizePolicy1.setHeightForWidth(self.load_extra_args_button.sizePolicy().hasHeightForWidth())
        self.load_extra_args_button.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.load_extra_args_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.scrollArea = QScrollArea(extra_fields_ui)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.extra_fields_item_widget = QWidget()
        self.extra_fields_item_widget.setObjectName(u"extra_fields_item_widget")
        self.extra_fields_item_widget.setGeometry(QRect(0, 0, 500, 599))
        self.verticalLayout_2 = QVBoxLayout(self.extra_fields_item_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea.setWidget(self.extra_fields_item_widget)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(extra_fields_ui)

        QMetaObject.connectSlotsByName(extra_fields_ui)
    # setupUi

    def retranslateUi(self, extra_fields_ui):
        extra_fields_ui.setWindowTitle(QCoreApplication.translate("extra_fields_ui", u"Form", None))
        self.add_extra_arg_button.setText(QCoreApplication.translate("extra_fields_ui", u"Add Arg", None))
        self.save_extra_args_button.setText("")
        self.load_extra_args_button.setText("")
    # retranslateUi

