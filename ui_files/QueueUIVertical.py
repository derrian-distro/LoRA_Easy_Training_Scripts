# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'QueueUIVertical.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QPushButton,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

from modules.LineEditHighlight import LineEditWithHighlight

class Ui_queue_ui(object):
    def setupUi(self, queue_ui):
        if not queue_ui.objectName():
            queue_ui.setObjectName(u"queue_ui")
        queue_ui.resize(150, 527)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(queue_ui.sizePolicy().hasHeightForWidth())
        queue_ui.setSizePolicy(sizePolicy)
        queue_ui.setMinimumSize(QSize(150, 0))
        queue_ui.setMaximumSize(QSize(150, 16777215))
        self.gridLayout = QGridLayout(queue_ui)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.top_arrow = QPushButton(queue_ui)
        self.top_arrow.setObjectName(u"top_arrow")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.top_arrow.sizePolicy().hasHeightForWidth())
        self.top_arrow.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.top_arrow, 0, 0, 1, 1)

        self.frame = QFrame(queue_ui)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.queue_scroll_area = QScrollArea(self.frame)
        self.queue_scroll_area.setObjectName(u"queue_scroll_area")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.queue_scroll_area.sizePolicy().hasHeightForWidth())
        self.queue_scroll_area.setSizePolicy(sizePolicy2)
        self.queue_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.queue_scroll_area.setWidgetResizable(True)
        self.queue_scroll_widget = QWidget()
        self.queue_scroll_widget.setObjectName(u"queue_scroll_widget")
        self.queue_scroll_widget.setGeometry(QRect(0, 0, 146, 373))
        self.verticalLayout_2 = QVBoxLayout(self.queue_scroll_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.queue_scroll_area.setWidget(self.queue_scroll_widget)

        self.verticalLayout.addWidget(self.queue_scroll_area)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.bottom_arrow = QPushButton(queue_ui)
        self.bottom_arrow.setObjectName(u"bottom_arrow")
        sizePolicy1.setHeightForWidth(self.bottom_arrow.sizePolicy().hasHeightForWidth())
        self.bottom_arrow.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.bottom_arrow, 2, 0, 1, 1)

        self.queue_name = LineEditWithHighlight(queue_ui)
        self.queue_name.setObjectName(u"queue_name")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.queue_name.sizePolicy().hasHeightForWidth())
        self.queue_name.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.queue_name, 3, 0, 1, 1)

        self.add_to_queue_button = QPushButton(queue_ui)
        self.add_to_queue_button.setObjectName(u"add_to_queue_button")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.add_to_queue_button.sizePolicy().hasHeightForWidth())
        self.add_to_queue_button.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.add_to_queue_button, 4, 0, 1, 1)

        self.remove_from_queue_button = QPushButton(queue_ui)
        self.remove_from_queue_button.setObjectName(u"remove_from_queue_button")
        sizePolicy3.setHeightForWidth(self.remove_from_queue_button.sizePolicy().hasHeightForWidth())
        self.remove_from_queue_button.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.remove_from_queue_button, 5, 0, 1, 1)


        self.retranslateUi(queue_ui)

        QMetaObject.connectSlotsByName(queue_ui)
    # setupUi

    def retranslateUi(self, queue_ui):
        queue_ui.setWindowTitle(QCoreApplication.translate("queue_ui", u"Form", None))
        self.top_arrow.setText("")
        self.bottom_arrow.setText("")
#if QT_CONFIG(tooltip)
        self.queue_name.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.queue_name.setPlaceholderText(QCoreApplication.translate("queue_ui", u"Queue Name", None))
        self.add_to_queue_button.setText(QCoreApplication.translate("queue_ui", u"Add", None))
        self.remove_from_queue_button.setText(QCoreApplication.translate("queue_ui", u"Remove", None))
    # retranslateUi

