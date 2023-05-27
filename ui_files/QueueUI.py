# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'QueueUI.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QPushButton, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

from modules.LineEditHighlight import LineEditWithHighlight

class Ui_queue_ui(object):
    def setupUi(self, queue_ui):
        if not queue_ui.objectName():
            queue_ui.setObjectName(u"queue_ui")
        queue_ui.resize(586, 90)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(queue_ui.sizePolicy().hasHeightForWidth())
        queue_ui.setSizePolicy(sizePolicy)
        queue_ui.setMinimumSize(QSize(477, 0))
        self.horizontalLayout = QHBoxLayout(queue_ui)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_arrow = QPushButton(queue_ui)
        self.left_arrow.setObjectName(u"left_arrow")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.left_arrow.sizePolicy().hasHeightForWidth())
        self.left_arrow.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.left_arrow)

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
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.queue_scroll_area.sizePolicy().hasHeightForWidth())
        self.queue_scroll_area.setSizePolicy(sizePolicy2)
        self.queue_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.queue_scroll_area.setWidgetResizable(True)
        self.queue_scroll_widget = QWidget()
        self.queue_scroll_widget.setObjectName(u"queue_scroll_widget")
        self.queue_scroll_widget.setGeometry(QRect(0, 0, 278, 68))
        self.horizontalLayout_2 = QHBoxLayout(self.queue_scroll_widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.queue_scroll_area.setWidget(self.queue_scroll_widget)

        self.verticalLayout.addWidget(self.queue_scroll_area)


        self.horizontalLayout.addWidget(self.frame)

        self.right_arrow = QPushButton(queue_ui)
        self.right_arrow.setObjectName(u"right_arrow")
        sizePolicy1.setHeightForWidth(self.right_arrow.sizePolicy().hasHeightForWidth())
        self.right_arrow.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.right_arrow)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.add_to_queue_button = QPushButton(queue_ui)
        self.add_to_queue_button.setObjectName(u"add_to_queue_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.add_to_queue_button.sizePolicy().hasHeightForWidth())
        self.add_to_queue_button.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.add_to_queue_button, 1, 1, 1, 1)

        self.queue_name = LineEditWithHighlight(queue_ui)
        self.queue_name.setObjectName(u"queue_name")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.queue_name.sizePolicy().hasHeightForWidth())
        self.queue_name.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.queue_name, 1, 0, 1, 1)

        self.remove_from_queue_button = QPushButton(queue_ui)
        self.remove_from_queue_button.setObjectName(u"remove_from_queue_button")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.remove_from_queue_button.sizePolicy().hasHeightForWidth())
        self.remove_from_queue_button.setSizePolicy(sizePolicy5)

        self.gridLayout.addWidget(self.remove_from_queue_button, 2, 0, 1, 2)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.retranslateUi(queue_ui)

        QMetaObject.connectSlotsByName(queue_ui)
    # setupUi

    def retranslateUi(self, queue_ui):
        queue_ui.setWindowTitle(QCoreApplication.translate("queue_ui", u"Form", None))
        self.left_arrow.setText("")
        self.right_arrow.setText("")
        self.add_to_queue_button.setText(QCoreApplication.translate("queue_ui", u"add to queue", None))
#if QT_CONFIG(tooltip)
        self.queue_name.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.queue_name.setPlaceholderText(QCoreApplication.translate("queue_ui", u"Queue Name", None))
        self.remove_from_queue_button.setText(QCoreApplication.translate("queue_ui", u"remove from queue", None))
    # retranslateUi

