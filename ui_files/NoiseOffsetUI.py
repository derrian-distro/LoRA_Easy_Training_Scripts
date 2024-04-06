# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NoiseOffsetUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QHBoxLayout,
    QLabel, QSizePolicy, QWidget)

from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (DoubleSpinBox, SpinBox)

class Ui_noise_offset_UI(object):
    def setupUi(self, noise_offset_UI):
        if not noise_offset_UI.objectName():
            noise_offset_UI.setObjectName(u"noise_offset_UI")
        noise_offset_UI.resize(400, 75)
        self.formLayout_2 = QFormLayout(noise_offset_UI)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.noise_offset_enable = QCheckBox(noise_offset_UI)
        self.noise_offset_enable.setObjectName(u"noise_offset_enable")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.noise_offset_enable)

        self.noise_offset_input = LineEditWithHighlight(noise_offset_UI)
        self.noise_offset_input.setObjectName(u"noise_offset_input")
        self.noise_offset_input.setEnabled(False)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.noise_offset_input)

        self.pyramid_noise_enable = QCheckBox(noise_offset_UI)
        self.pyramid_noise_enable.setObjectName(u"pyramid_noise_enable")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.pyramid_noise_enable)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(noise_offset_UI)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.pyramid_iteration_input = SpinBox(noise_offset_UI)
        self.pyramid_iteration_input.setObjectName(u"pyramid_iteration_input")
        self.pyramid_iteration_input.setEnabled(False)
        self.pyramid_iteration_input.setFocusPolicy(Qt.StrongFocus)
        self.pyramid_iteration_input.setMinimum(1)
        self.pyramid_iteration_input.setValue(6)

        self.horizontalLayout.addWidget(self.pyramid_iteration_input)

        self.label_3 = QLabel(noise_offset_UI)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.pyramid_discount_input = DoubleSpinBox(noise_offset_UI)
        self.pyramid_discount_input.setObjectName(u"pyramid_discount_input")
        self.pyramid_discount_input.setEnabled(False)
        self.pyramid_discount_input.setFocusPolicy(Qt.StrongFocus)
        self.pyramid_discount_input.setMinimum(0.010000000000000)
        self.pyramid_discount_input.setSingleStep(0.010000000000000)
        self.pyramid_discount_input.setValue(0.300000000000000)

        self.horizontalLayout.addWidget(self.pyramid_discount_input)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)


        self.retranslateUi(noise_offset_UI)

        QMetaObject.connectSlotsByName(noise_offset_UI)
    # setupUi

    def retranslateUi(self, noise_offset_UI):
        noise_offset_UI.setWindowTitle(QCoreApplication.translate("noise_offset_UI", u"Form", None))
        self.noise_offset_enable.setText(QCoreApplication.translate("noise_offset_UI", u"Noise Offset", None))
        self.noise_offset_input.setText(QCoreApplication.translate("noise_offset_UI", u"0.1", None))
        self.pyramid_noise_enable.setText(QCoreApplication.translate("noise_offset_UI", u"Pyramid Noise", None))
        self.label_2.setText(QCoreApplication.translate("noise_offset_UI", u"Iterations", None))
#if QT_CONFIG(tooltip)
        self.pyramid_iteration_input.setToolTip(QCoreApplication.translate("noise_offset_UI", u"<html><head/><body><p>The number of iterations. It is said that the values in 6-10 work best.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("noise_offset_UI", u"Discount", None))
#if QT_CONFIG(tooltip)
        self.pyramid_discount_input.setToolTip(QCoreApplication.translate("noise_offset_UI", u"<html><head/><body><p>Not entirely sure what this is, but the recommended value is 0.1-0.3.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

