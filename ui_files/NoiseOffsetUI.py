# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NoiseOffsetUI.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox)

class Ui_noise_offset_UI(object):
    def setupUi(self, noise_offset_UI):
        if not noise_offset_UI.objectName():
            noise_offset_UI.setObjectName(u"noise_offset_UI")
        noise_offset_UI.resize(400, 178)
        self.verticalLayout = QVBoxLayout(noise_offset_UI)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.noise_offset_group = QGroupBox(noise_offset_UI)
        self.noise_offset_group.setObjectName(u"noise_offset_group")
        self.noise_offset_group.setCheckable(True)
        self.noise_offset_group.setChecked(False)
        self.formLayout = QFormLayout(self.noise_offset_group)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.noise_offset_group)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.noise_offset_selector = ComboBox(self.noise_offset_group)
        self.noise_offset_selector.addItem("")
        self.noise_offset_selector.addItem("")
        self.noise_offset_selector.setObjectName(u"noise_offset_selector")
        self.noise_offset_selector.setFocusPolicy(Qt.StrongFocus)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.noise_offset_selector)

        self.label_2 = QLabel(self.noise_offset_group)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.noise_offset_group)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.pyramid_iteration_input = SpinBox(self.noise_offset_group)
        self.pyramid_iteration_input.setObjectName(u"pyramid_iteration_input")
        self.pyramid_iteration_input.setFocusPolicy(Qt.StrongFocus)
        self.pyramid_iteration_input.setMinimum(1)
        self.pyramid_iteration_input.setValue(6)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.pyramid_iteration_input)

        self.pyramid_discount_input = DoubleSpinBox(self.noise_offset_group)
        self.pyramid_discount_input.setObjectName(u"pyramid_discount_input")
        self.pyramid_discount_input.setFocusPolicy(Qt.StrongFocus)
        self.pyramid_discount_input.setMinimum(0.010000000000000)
        self.pyramid_discount_input.setSingleStep(0.010000000000000)
        self.pyramid_discount_input.setValue(0.300000000000000)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.pyramid_discount_input)

        self.noise_offset_input = LineEditWithHighlight(self.noise_offset_group)
        self.noise_offset_input.setObjectName(u"noise_offset_input")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.noise_offset_input)


        self.verticalLayout.addWidget(self.noise_offset_group)


        self.retranslateUi(noise_offset_UI)

        QMetaObject.connectSlotsByName(noise_offset_UI)
    # setupUi

    def retranslateUi(self, noise_offset_UI):
        noise_offset_UI.setWindowTitle(QCoreApplication.translate("noise_offset_UI", u"Form", None))
        self.noise_offset_group.setTitle(QCoreApplication.translate("noise_offset_UI", u"Enable", None))
        self.label.setText(QCoreApplication.translate("noise_offset_UI", u"Noise Offset Value", None))
        self.noise_offset_selector.setItemText(0, QCoreApplication.translate("noise_offset_UI", u"Normal", None))
        self.noise_offset_selector.setItemText(1, QCoreApplication.translate("noise_offset_UI", u"Pyramid", None))

#if QT_CONFIG(tooltip)
        self.noise_offset_selector.setToolTip(QCoreApplication.translate("noise_offset_UI", u"<html><head/><body><p>Noise offset comes in two varieties, normal, and pyramid. Normal works, but has the issue of not having great compatability. Pyramid seems to work about as well, and not have a big impact on compatability.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("noise_offset_UI", u"Pyramid Iterations", None))
        self.label_3.setText(QCoreApplication.translate("noise_offset_UI", u"Pyramid Discount", None))
#if QT_CONFIG(tooltip)
        self.pyramid_iteration_input.setToolTip(QCoreApplication.translate("noise_offset_UI", u"<html><head/><body><p>The number of iterations. It is said that the values in 6-10 work best.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pyramid_discount_input.setToolTip(QCoreApplication.translate("noise_offset_UI", u"<html><head/><body><p>Not entirely sure what this is, but the recommended value is 0.1-0.3.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.noise_offset_input.setText(QCoreApplication.translate("noise_offset_UI", u"0.1", None))
    # retranslateUi

