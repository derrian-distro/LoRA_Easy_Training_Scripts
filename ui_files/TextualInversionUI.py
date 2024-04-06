# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TextualInversionUI.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import SpinBox

class Ui_textual_inversion_ui(object):
    def setupUi(self, textual_inversion_ui):
        if not textual_inversion_ui.objectName():
            textual_inversion_ui.setObjectName(u"textual_inversion_ui")
        textual_inversion_ui.resize(424, 150)
        self.verticalLayout = QVBoxLayout(textual_inversion_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.token_group = QGroupBox(textual_inversion_ui)
        self.token_group.setObjectName(u"token_group")
        self.token_group.setCheckable(False)
        self.token_group.setChecked(False)
        self.formLayout = QFormLayout(self.token_group)
        self.formLayout.setObjectName(u"formLayout")
        self.token_label = QLabel(self.token_group)
        self.token_label.setObjectName(u"token_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.token_label)

        self.token_string = LineEditWithHighlight(self.token_group)
        self.token_string.setObjectName(u"token_string")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.token_string)

        self.init_word_label = QLabel(self.token_group)
        self.init_word_label.setObjectName(u"init_word_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.init_word_label)

        self.init_word = LineEditWithHighlight(self.token_group)
        self.init_word.setObjectName(u"init_word")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.init_word)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.num_vectors_per_token = SpinBox(self.token_group)
        self.num_vectors_per_token.setObjectName(u"num_vectors_per_token")
        self.num_vectors_per_token.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.num_vectors_per_token.sizePolicy().hasHeightForWidth())
        self.num_vectors_per_token.setSizePolicy(sizePolicy)
        self.num_vectors_per_token.setFocusPolicy(Qt.StrongFocus)
        self.num_vectors_per_token.setMinimum(0)
        self.num_vectors_per_token.setMaximum(16777215)
        self.num_vectors_per_token.setValue(0)

        self.horizontalLayout.addWidget(self.num_vectors_per_token)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.vectors_per_token_enable = QCheckBox(self.token_group)
        self.vectors_per_token_enable.setObjectName(u"vectors_per_token_enable")
        self.vectors_per_token_enable.setEnabled(True)
        self.vectors_per_token_enable.setTristate(False)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.vectors_per_token_enable)


        self.verticalLayout.addWidget(self.token_group)


        self.retranslateUi(textual_inversion_ui)

        QMetaObject.connectSlotsByName(textual_inversion_ui)
    # setupUi

    def retranslateUi(self, textual_inversion_ui):
        textual_inversion_ui.setWindowTitle(QCoreApplication.translate("textual_inversion_ui", u"Form", None))
        self.token_group.setTitle("")
        self.token_label.setText(QCoreApplication.translate("textual_inversion_ui", u"Token String", None))
#if QT_CONFIG(tooltip)
        self.init_word_label.setToolTip(QCoreApplication.translate("textual_inversion_ui", u"<html><head/><body><p>Initial token string.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.init_word_label.setText(QCoreApplication.translate("textual_inversion_ui", u"Initial Word", None))
#if QT_CONFIG(tooltip)
        self.num_vectors_per_token.setToolTip(QCoreApplication.translate("textual_inversion_ui", u"<html><head/><body><p>The amount of time between samples. I personally suggest you have it generate a sample every epoch, however, again, personal preference.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.vectors_per_token_enable.setText(QCoreApplication.translate("textual_inversion_ui", u"Vectors per Token", None))
    # retranslateUi

