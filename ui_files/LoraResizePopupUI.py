# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoraResizePopupUI.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFormLayout,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

from modules.DragDropLineEdit import DragDropLineEdit
from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox)

class Ui_lora_resize_ui(object):
    def setupUi(self, lora_resize_ui):
        if not lora_resize_ui.objectName():
            lora_resize_ui.setObjectName(u"lora_resize_ui")
        lora_resize_ui.resize(483, 293)
        self.gridLayout = QGridLayout(lora_resize_ui)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_3 = QLabel(lora_resize_ui)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.label = QLabel(lora_resize_ui)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.save_precision_select = ComboBox(lora_resize_ui)
        self.save_precision_select.addItem("")
        self.save_precision_select.addItem("")
        self.save_precision_select.addItem("")
        self.save_precision_select.setObjectName(u"save_precision_select")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.save_precision_select)

        self.new_rank_label = QLabel(lora_resize_ui)
        self.new_rank_label.setObjectName(u"new_rank_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.new_rank_label)

        self.new_rank_input = SpinBox(lora_resize_ui)
        self.new_rank_input.setObjectName(u"new_rank_input")
        self.new_rank_input.setMinimum(1)
        self.new_rank_input.setValue(4)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.new_rank_input)

        self.new_conv_enable = QCheckBox(lora_resize_ui)
        self.new_conv_enable.setObjectName(u"new_conv_enable")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.new_conv_enable)

        self.new_conv_rank_input = SpinBox(lora_resize_ui)
        self.new_conv_rank_input.setObjectName(u"new_conv_rank_input")
        self.new_conv_rank_input.setEnabled(False)
        self.new_conv_rank_input.setMinimum(1)
        self.new_conv_rank_input.setValue(1)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.new_conv_rank_input)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.output_folder_input = DragDropLineEdit(lora_resize_ui)
        self.output_folder_input.setObjectName(u"output_folder_input")
        self.output_folder_input.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.output_folder_input)

        self.output_folder_selector = QPushButton(lora_resize_ui)
        self.output_folder_selector.setObjectName(u"output_folder_selector")
        self.output_folder_selector.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.output_folder_selector)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.output_name_input = LineEditWithHighlight(lora_resize_ui)
        self.output_name_input.setObjectName(u"output_name_input")
        self.output_name_input.setEnabled(False)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.output_name_input)

        self.dynamic_param_enable = QCheckBox(lora_resize_ui)
        self.dynamic_param_enable.setObjectName(u"dynamic_param_enable")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.dynamic_param_enable)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.dynamic_param_select = ComboBox(lora_resize_ui)
        self.dynamic_param_select.addItem("")
        self.dynamic_param_select.addItem("")
        self.dynamic_param_select.addItem("")
        self.dynamic_param_select.setObjectName(u"dynamic_param_select")
        self.dynamic_param_select.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.dynamic_param_select)

        self.dynamic_param_input = DoubleSpinBox(lora_resize_ui)
        self.dynamic_param_input.setObjectName(u"dynamic_param_input")
        self.dynamic_param_input.setEnabled(False)
        self.dynamic_param_input.setDecimals(4)
        self.dynamic_param_input.setMinimum(0.000100000000000)
        self.dynamic_param_input.setMaximum(1.000000000000000)
        self.dynamic_param_input.setSingleStep(0.010000000000000)
        self.dynamic_param_input.setValue(0.970000000000000)

        self.horizontalLayout_3.addWidget(self.dynamic_param_input)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.use_gpu_enable = QCheckBox(lora_resize_ui)
        self.use_gpu_enable.setObjectName(u"use_gpu_enable")
        self.use_gpu_enable.setChecked(True)

        self.horizontalLayout_4.addWidget(self.use_gpu_enable)

        self.verbose_enable = QCheckBox(lora_resize_ui)
        self.verbose_enable.setObjectName(u"verbose_enable")

        self.horizontalLayout_4.addWidget(self.verbose_enable)

        self.remove_conv_dims_enable = QCheckBox(lora_resize_ui)
        self.remove_conv_dims_enable.setObjectName(u"remove_conv_dims_enable")

        self.horizontalLayout_4.addWidget(self.remove_conv_dims_enable)

        self.remove_linear_dims_enable = QCheckBox(lora_resize_ui)
        self.remove_linear_dims_enable.setObjectName(u"remove_linear_dims_enable")

        self.horizontalLayout_4.addWidget(self.remove_linear_dims_enable)


        self.formLayout.setLayout(7, QFormLayout.SpanningRole, self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.model_input = DragDropLineEdit(lora_resize_ui)
        self.model_input.setObjectName(u"model_input")

        self.horizontalLayout.addWidget(self.model_input)

        self.model_input_selector = QPushButton(lora_resize_ui)
        self.model_input_selector.setObjectName(u"model_input_selector")

        self.horizontalLayout.addWidget(self.model_input_selector)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.output_folder_enable = QCheckBox(lora_resize_ui)
        self.output_folder_enable.setObjectName(u"output_folder_enable")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.output_folder_enable)

        self.output_name_enable = QCheckBox(lora_resize_ui)
        self.output_name_enable.setObjectName(u"output_name_enable")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.output_name_enable)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.begin_resize_button = QPushButton(lora_resize_ui)
        self.begin_resize_button.setObjectName(u"begin_resize_button")

        self.gridLayout.addWidget(self.begin_resize_button, 1, 0, 1, 1)


        self.retranslateUi(lora_resize_ui)

        QMetaObject.connectSlotsByName(lora_resize_ui)
    # setupUi

    def retranslateUi(self, lora_resize_ui):
        lora_resize_ui.setWindowTitle(QCoreApplication.translate("lora_resize_ui", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("lora_resize_ui", u"Model", None))
        self.label.setText(QCoreApplication.translate("lora_resize_ui", u"Save Precision", None))
        self.save_precision_select.setItemText(0, QCoreApplication.translate("lora_resize_ui", u"fp16", None))
        self.save_precision_select.setItemText(1, QCoreApplication.translate("lora_resize_ui", u"bf16", None))
        self.save_precision_select.setItemText(2, QCoreApplication.translate("lora_resize_ui", u"float", None))

        self.new_rank_label.setText(QCoreApplication.translate("lora_resize_ui", u"New Rank", None))
        self.new_conv_enable.setText(QCoreApplication.translate("lora_resize_ui", u"New Conv Rank", None))
        self.output_folder_selector.setText("")
        self.dynamic_param_enable.setText(QCoreApplication.translate("lora_resize_ui", u"Dynamic Method", None))
        self.dynamic_param_select.setItemText(0, QCoreApplication.translate("lora_resize_ui", u"sv_fro", None))
        self.dynamic_param_select.setItemText(1, QCoreApplication.translate("lora_resize_ui", u"sv_ratio", None))
        self.dynamic_param_select.setItemText(2, QCoreApplication.translate("lora_resize_ui", u"sv_cumulative", None))

        self.use_gpu_enable.setText(QCoreApplication.translate("lora_resize_ui", u"Use GPU", None))
        self.verbose_enable.setText(QCoreApplication.translate("lora_resize_ui", u"Verbose Printing", None))
        self.remove_conv_dims_enable.setText(QCoreApplication.translate("lora_resize_ui", u"Remove Conv Dims", None))
        self.remove_linear_dims_enable.setText(QCoreApplication.translate("lora_resize_ui", u"Remove Linear Dims", None))
        self.model_input_selector.setText("")
        self.output_folder_enable.setText(QCoreApplication.translate("lora_resize_ui", u"Output Folder", None))
        self.output_name_enable.setText(QCoreApplication.translate("lora_resize_ui", u"Output Name", None))
        self.begin_resize_button.setText(QCoreApplication.translate("lora_resize_ui", u"Start Resizing", None))
    # retranslateUi

