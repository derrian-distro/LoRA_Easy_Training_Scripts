# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TextualInversionUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import SpinBox

class Ui_textual_inversion_ui(object):
    def setupUi(self, textual_inversion_ui):
        if not textual_inversion_ui.objectName():
            textual_inversion_ui.setObjectName(u"textual_inversion_ui")
        textual_inversion_ui.resize(424, 105)
        self.verticalLayout = QVBoxLayout(textual_inversion_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label = QLabel(textual_inversion_ui)
        self.label.setObjectName(u"label")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(textual_inversion_ui)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.token_string_input = LineEditWithHighlight(textual_inversion_ui)
        self.token_string_input.setObjectName(u"token_string_input")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.token_string_input)

        self.initial_word_input = LineEditWithHighlight(textual_inversion_ui)
        self.initial_word_input.setObjectName(u"initial_word_input")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.initial_word_input)

        self.vectors_per_token_input = SpinBox(textual_inversion_ui)
        self.vectors_per_token_input.setObjectName(u"vectors_per_token_input")
        self.vectors_per_token_input.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vectors_per_token_input.sizePolicy().hasHeightForWidth())
        self.vectors_per_token_input.setSizePolicy(sizePolicy)
        self.vectors_per_token_input.setFocusPolicy(Qt.StrongFocus)
        self.vectors_per_token_input.setMinimum(0)
        self.vectors_per_token_input.setMaximum(16777215)
        self.vectors_per_token_input.setValue(0)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.vectors_per_token_input)

        self.vectors_per_token_enable = QCheckBox(textual_inversion_ui)
        self.vectors_per_token_enable.setObjectName(u"vectors_per_token_enable")
        self.vectors_per_token_enable.setEnabled(True)
        self.vectors_per_token_enable.setTristate(False)

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.vectors_per_token_enable)


        self.verticalLayout.addLayout(self.formLayout_3)


        self.retranslateUi(textual_inversion_ui)

        QMetaObject.connectSlotsByName(textual_inversion_ui)
    # setupUi

    def retranslateUi(self, textual_inversion_ui):
        textual_inversion_ui.setWindowTitle(QCoreApplication.translate("textual_inversion_ui", u"Form", None))
        self.label.setText(QCoreApplication.translate("textual_inversion_ui", u"Token String", None))
        self.label_2.setText(QCoreApplication.translate("textual_inversion_ui", u"Initial Word", None))
#if QT_CONFIG(tooltip)
        self.vectors_per_token_input.setToolTip(QCoreApplication.translate("textual_inversion_ui", u"<html><head/><body><p>The number of new vectors to train for the embedding. By default, equal to the number of tokens in the initial token string.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.vectors_per_token_enable.setText(QCoreApplication.translate("textual_inversion_ui", u"Vectors per Token", None))
    # retranslateUi

