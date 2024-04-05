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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (ComboBox, SpinBox)

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

        self.init_word_label = QLabel(self.token_group)
        self.init_word_label.setObjectName(u"init_word")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.init_word_label)

        self.steps_label = QLabel(self.token_group)
        self.steps_label.setObjectName(u"steps_label")
        self.steps_label.setEnabled(False)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.steps_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.test = ComboBox(self.token_group)
        self.test.addItem("")
        self.test.addItem("")
        self.test.setObjectName(u"test")
        self.test.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.test.sizePolicy().hasHeightForWidth())
        self.test.setSizePolicy(sizePolicy)
        self.test.setFocusPolicy(Qt.StrongFocus)

        self.horizontalLayout.addWidget(self.test)

        self.disable = SpinBox(self.token_group)
        self.disable.setObjectName(u"disable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.disable.sizePolicy().hasHeightForWidth())
        self.disable.setSizePolicy(sizePolicy1)
        self.disable.setFocusPolicy(Qt.StrongFocus)
        self.disable.setMinimum(1)
        self.disable.setMaximum(16777215)
        self.disable.setValue(1)

        self.horizontalLayout.addWidget(self.disable)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.init_word = LineEditWithHighlight(self.token_group)
        self.init_word.setObjectName(u"init_word")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.init_word)

        self.token_string = LineEditWithHighlight(self.token_group)
        self.token_string.setObjectName(u"token_string")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.token_string)


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
        self.steps_label.setText(QCoreApplication.translate("textual_inversion_ui", u"Time Between Sample", None))
        self.test.setItemText(0, QCoreApplication.translate("textual_inversion_ui", u"Steps Per Sample", None))
        self.test.setItemText(1, QCoreApplication.translate("textual_inversion_ui", u"Epochs Per Sample", None))

#if QT_CONFIG(tooltip)
        self.test.setToolTip(QCoreApplication.translate("textual_inversion_ui", u"<html><head/><body><p>The amount of time between samples. I personally suggest you have it generate a sample every epoch, however, again, personal preference.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.disable.setToolTip(QCoreApplication.translate("textual_inversion_ui", u"<html><head/><body><p>The amount of time between samples. I personally suggest you have it generate a sample every epoch, however, again, personal preference.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

