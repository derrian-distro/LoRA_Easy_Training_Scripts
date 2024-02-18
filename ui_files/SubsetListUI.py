# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SubsetListUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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

from modules.LineEditHighlight import LineEditWithHighlight

class Ui_subset_list_ui(object):
    def setupUi(self, subset_list_ui):
        if not subset_list_ui.objectName():
            subset_list_ui.setObjectName(u"subset_list_ui")
        subset_list_ui.resize(600, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(subset_list_ui.sizePolicy().hasHeightForWidth())
        subset_list_ui.setSizePolicy(sizePolicy)
        subset_list_ui.setMinimumSize(QSize(600, 300))
        self.verticalLayout_2 = QVBoxLayout(subset_list_ui)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.add_bulk_button = QPushButton(subset_list_ui)
        self.add_bulk_button.setObjectName(u"add_bulk_button")

        self.verticalLayout_2.addWidget(self.add_bulk_button)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.add_subset_name_input = LineEditWithHighlight(subset_list_ui)
        self.add_subset_name_input.setObjectName(u"add_subset_name_input")
        self.add_subset_name_input.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.add_subset_name_input)

        self.add_subset_button = QPushButton(subset_list_ui)
        self.add_subset_button.setObjectName(u"add_subset_button")

        self.horizontalLayout.addWidget(self.add_subset_button)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.subset_scroll_area = QScrollArea(subset_list_ui)
        self.subset_scroll_area.setObjectName(u"subset_scroll_area")
        self.subset_scroll_area.setWidgetResizable(True)
        self.subset_scroll_area.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.subset_scroll_area_content = QWidget()
        self.subset_scroll_area_content.setObjectName(u"subset_scroll_area_content")
        self.subset_scroll_area_content.setGeometry(QRect(0, 0, 580, 218))
        self.verticalLayout = QVBoxLayout(self.subset_scroll_area_content)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.subset_scroll_area.setWidget(self.subset_scroll_area_content)

        self.verticalLayout_2.addWidget(self.subset_scroll_area)


        self.retranslateUi(subset_list_ui)

        QMetaObject.connectSlotsByName(subset_list_ui)
    # setupUi

    def retranslateUi(self, subset_list_ui):
        subset_list_ui.setWindowTitle(QCoreApplication.translate("subset_list_ui", u"Form", None))
        self.add_bulk_button.setText(QCoreApplication.translate("subset_list_ui", u"Add All Subfolders From Folder", None))
        self.add_subset_name_input.setPlaceholderText(QCoreApplication.translate("subset_list_ui", u"Subset Name", None))
        self.add_subset_button.setText(QCoreApplication.translate("subset_list_ui", u"Add Subset", None))
    # retranslateUi

