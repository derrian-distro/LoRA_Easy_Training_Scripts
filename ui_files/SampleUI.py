# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SampleUI.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

from modules.DragDropLineEdit import DragDropLineEdit
from modules.ScrollOnSelect import (ComboBox, SpinBox)

class Ui_sample_ui(object):
    def setupUi(self, sample_ui):
        if not sample_ui.objectName():
            sample_ui.setObjectName(u"sample_ui")
        sample_ui.resize(400, 150)
        self.verticalLayout = QVBoxLayout(sample_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sample_group = QGroupBox(sample_ui)
        self.sample_group.setObjectName(u"sample_group")
        self.sample_group.setCheckable(True)
        self.sample_group.setChecked(False)
        self.formLayout = QFormLayout(self.sample_group)
        self.formLayout.setObjectName(u"formLayout")
        self.sampler_label = QLabel(self.sample_group)
        self.sampler_label.setObjectName(u"sampler_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.sampler_label)

        self.sampler_input = ComboBox(self.sample_group)
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.addItem("")
        self.sampler_input.setObjectName(u"sampler_input")
        self.sampler_input.setFocusPolicy(Qt.StrongFocus)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sampler_input)

        self.steps_label = QLabel(self.sample_group)
        self.steps_label.setObjectName(u"steps_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.steps_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.steps_epochs_selector = ComboBox(self.sample_group)
        self.steps_epochs_selector.addItem("")
        self.steps_epochs_selector.addItem("")
        self.steps_epochs_selector.setObjectName(u"steps_epochs_selector")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.steps_epochs_selector.sizePolicy().hasHeightForWidth())
        self.steps_epochs_selector.setSizePolicy(sizePolicy)
        self.steps_epochs_selector.setFocusPolicy(Qt.StrongFocus)

        self.horizontalLayout.addWidget(self.steps_epochs_selector)

        self.steps_epoch_input = SpinBox(self.sample_group)
        self.steps_epoch_input.setObjectName(u"steps_epoch_input")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.steps_epoch_input.sizePolicy().hasHeightForWidth())
        self.steps_epoch_input.setSizePolicy(sizePolicy1)
        self.steps_epoch_input.setFocusPolicy(Qt.StrongFocus)
        self.steps_epoch_input.setMinimum(1)
        self.steps_epoch_input.setMaximum(16777215)
        self.steps_epoch_input.setValue(1)

        self.horizontalLayout.addWidget(self.steps_epoch_input)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        self.text_file_label = QLabel(self.sample_group)
        self.text_file_label.setObjectName(u"text_file_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.text_file_label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.sample_prompt_txt_file_input = DragDropLineEdit(self.sample_group)
        self.sample_prompt_txt_file_input.setObjectName(u"sample_prompt_txt_file_input")

        self.horizontalLayout_2.addWidget(self.sample_prompt_txt_file_input)

        self.sample_prompt_selector = QPushButton(self.sample_group)
        self.sample_prompt_selector.setObjectName(u"sample_prompt_selector")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sample_prompt_selector.sizePolicy().hasHeightForWidth())
        self.sample_prompt_selector.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.sample_prompt_selector)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.sample_group)


        self.retranslateUi(sample_ui)

        QMetaObject.connectSlotsByName(sample_ui)
    # setupUi

    def retranslateUi(self, sample_ui):
        sample_ui.setWindowTitle(QCoreApplication.translate("sample_ui", u"Form", None))
        self.sample_group.setTitle(QCoreApplication.translate("sample_ui", u"Enable", None))
        self.sampler_label.setText(QCoreApplication.translate("sample_ui", u"Sampler ", None))
        self.sampler_input.setItemText(0, QCoreApplication.translate("sample_ui", u"DDIM", None))
        self.sampler_input.setItemText(1, QCoreApplication.translate("sample_ui", u"PNDM", None))
        self.sampler_input.setItemText(2, QCoreApplication.translate("sample_ui", u"LMS", None))
        self.sampler_input.setItemText(3, QCoreApplication.translate("sample_ui", u"EULER", None))
        self.sampler_input.setItemText(4, QCoreApplication.translate("sample_ui", u"EULER_A", None))
        self.sampler_input.setItemText(5, QCoreApplication.translate("sample_ui", u"HEUN", None))
        self.sampler_input.setItemText(6, QCoreApplication.translate("sample_ui", u"DPM_2", None))
        self.sampler_input.setItemText(7, QCoreApplication.translate("sample_ui", u"DPM_2_A", None))
        self.sampler_input.setItemText(8, QCoreApplication.translate("sample_ui", u"DPMSOLVER", None))
        self.sampler_input.setItemText(9, QCoreApplication.translate("sample_ui", u"DPMSOLVER++", None))
        self.sampler_input.setItemText(10, QCoreApplication.translate("sample_ui", u"DPMSINGLE", None))
        self.sampler_input.setItemText(11, QCoreApplication.translate("sample_ui", u"K_LMS", None))
        self.sampler_input.setItemText(12, QCoreApplication.translate("sample_ui", u"K_EULER", None))
        self.sampler_input.setItemText(13, QCoreApplication.translate("sample_ui", u"K_EULER_A", None))
        self.sampler_input.setItemText(14, QCoreApplication.translate("sample_ui", u"K_DPM_2", None))
        self.sampler_input.setItemText(15, QCoreApplication.translate("sample_ui", u"K_DPM_2_A", None))

#if QT_CONFIG(tooltip)
        self.sampler_input.setToolTip(QCoreApplication.translate("sample_ui", u"<html><head/><body><p>The Sampler used when generating test images. I personally suggest using either DDIM or Euler A, however it's really just personal preference.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.steps_label.setText(QCoreApplication.translate("sample_ui", u"Time Between Sample", None))
        self.steps_epochs_selector.setItemText(0, QCoreApplication.translate("sample_ui", u"Steps Per Sample", None))
        self.steps_epochs_selector.setItemText(1, QCoreApplication.translate("sample_ui", u"Epochs Per Sample", None))

#if QT_CONFIG(tooltip)
        self.steps_epochs_selector.setToolTip(QCoreApplication.translate("sample_ui", u"<html><head/><body><p>The amount of time between samples. I personally suggest you have it generate a sample every epoch, however, again, personal preference.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.steps_epoch_input.setToolTip(QCoreApplication.translate("sample_ui", u"<html><head/><body><p>The amount of time between samples. I personally suggest you have it generate a sample every epoch, however, again, personal preference.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.text_file_label.setText(QCoreApplication.translate("sample_ui", u"Prompt Text File", None))
#if QT_CONFIG(tooltip)
        self.sample_prompt_txt_file_input.setToolTip(QCoreApplication.translate("sample_ui", u"<html><head/><body><p>The input file that contains all of your prompts. This file must be a txt file and have one prompt per line. you can specify a bunch of args within each line for things like negative prompts, width and height, and more. For documentation on this please visit the sd-scripts github repo.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.sample_prompt_txt_file_input.setPlaceholderText(QCoreApplication.translate("sample_ui", u"Text File", None))
        self.sample_prompt_selector.setText("")
    # retranslateUi

