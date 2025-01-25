# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FluxUI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

from modules.DragDropLineEdit import DragDropLineEdit
from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox)

class Ui_flux_ui(object):
    def setupUi(self, flux_ui):
        if not flux_ui.objectName():
            flux_ui.setObjectName(u"flux_ui")
        flux_ui.resize(529, 317)
        self.gridLayout = QGridLayout(flux_ui)
        self.gridLayout.setObjectName(u"gridLayout")
        self.flux_training_box = QGroupBox(flux_ui)
        self.flux_training_box.setObjectName(u"flux_training_box")
        self.flux_training_box.setCheckable(True)
        self.flux_training_box.setChecked(False)
        self.gridLayout_2 = QGridLayout(self.flux_training_box)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label = QLabel(self.flux_training_box)
        self.label.setObjectName(u"label")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ae_model_input = DragDropLineEdit(self.flux_training_box)
        self.ae_model_input.setObjectName(u"ae_model_input")

        self.horizontalLayout.addWidget(self.ae_model_input)

        self.ae_model_selector = QPushButton(self.flux_training_box)
        self.ae_model_selector.setObjectName(u"ae_model_selector")

        self.horizontalLayout.addWidget(self.ae_model_selector)


        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_2 = QLabel(self.flux_training_box)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.clip_l_model_input = DragDropLineEdit(self.flux_training_box)
        self.clip_l_model_input.setObjectName(u"clip_l_model_input")

        self.horizontalLayout_2.addWidget(self.clip_l_model_input)

        self.clip_l_model_selector = QPushButton(self.flux_training_box)
        self.clip_l_model_selector.setObjectName(u"clip_l_model_selector")

        self.horizontalLayout_2.addWidget(self.clip_l_model_selector)


        self.formLayout_3.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_3 = QLabel(self.flux_training_box)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.t5_model_input = DragDropLineEdit(self.flux_training_box)
        self.t5_model_input.setObjectName(u"t5_model_input")

        self.horizontalLayout_3.addWidget(self.t5_model_input)

        self.t5_model_selector = QPushButton(self.flux_training_box)
        self.t5_model_selector.setObjectName(u"t5_model_selector")

        self.horizontalLayout_3.addWidget(self.t5_model_selector)


        self.formLayout_3.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.apply_t5_attention_mask_enable = QCheckBox(self.flux_training_box)
        self.apply_t5_attention_mask_enable.setObjectName(u"apply_t5_attention_mask_enable")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apply_t5_attention_mask_enable.sizePolicy().hasHeightForWidth())
        self.apply_t5_attention_mask_enable.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.apply_t5_attention_mask_enable)

        self.label_4 = QLabel(self.flux_training_box)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_4.addWidget(self.label_4)

        self.t5_max_token_input = SpinBox(self.flux_training_box)
        self.t5_max_token_input.setObjectName(u"t5_max_token_input")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.t5_max_token_input.sizePolicy().hasHeightForWidth())
        self.t5_max_token_input.setSizePolicy(sizePolicy1)
        self.t5_max_token_input.setMaximum(16777215)
        self.t5_max_token_input.setValue(512)

        self.horizontalLayout_4.addWidget(self.t5_max_token_input)

        self.label_12 = QLabel(self.flux_training_box)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_4.addWidget(self.label_12)

        self.guidance_scale_input = DoubleSpinBox(self.flux_training_box)
        self.guidance_scale_input.setObjectName(u"guidance_scale_input")
        self.guidance_scale_input.setDecimals(4)
        self.guidance_scale_input.setSingleStep(0.100000000000000)
        self.guidance_scale_input.setValue(1.000000000000000)

        self.horizontalLayout_4.addWidget(self.guidance_scale_input)


        self.formLayout_3.setLayout(3, QFormLayout.SpanningRole, self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.split_mode_enable = QCheckBox(self.flux_training_box)
        self.split_mode_enable.setObjectName(u"split_mode_enable")
        sizePolicy1.setHeightForWidth(self.split_mode_enable.sizePolicy().hasHeightForWidth())
        self.split_mode_enable.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.split_mode_enable)

        self.label_6 = QLabel(self.flux_training_box)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.timestep_sampling_selector = ComboBox(self.flux_training_box)
        self.timestep_sampling_selector.addItem("")
        self.timestep_sampling_selector.addItem("")
        self.timestep_sampling_selector.addItem("")
        self.timestep_sampling_selector.addItem("")
        self.timestep_sampling_selector.addItem("")
        self.timestep_sampling_selector.setObjectName(u"timestep_sampling_selector")

        self.horizontalLayout_5.addWidget(self.timestep_sampling_selector)

        self.label_5 = QLabel(self.flux_training_box)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.weighting_scheme_selector = ComboBox(self.flux_training_box)
        self.weighting_scheme_selector.addItem("")
        self.weighting_scheme_selector.addItem("")
        self.weighting_scheme_selector.addItem("")
        self.weighting_scheme_selector.addItem("")
        self.weighting_scheme_selector.addItem("")
        self.weighting_scheme_selector.setObjectName(u"weighting_scheme_selector")

        self.horizontalLayout_5.addWidget(self.weighting_scheme_selector)


        self.formLayout_3.setLayout(4, QFormLayout.SpanningRole, self.horizontalLayout_5)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_8 = QLabel(self.flux_training_box)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_14.addWidget(self.label_8)

        self.logit_mean_input = DoubleSpinBox(self.flux_training_box)
        self.logit_mean_input.setObjectName(u"logit_mean_input")
        self.logit_mean_input.setDecimals(4)
        self.logit_mean_input.setSingleStep(0.010000000000000)

        self.horizontalLayout_14.addWidget(self.logit_mean_input)

        self.label_9 = QLabel(self.flux_training_box)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_14.addWidget(self.label_9)

        self.logit_std_input = DoubleSpinBox(self.flux_training_box)
        self.logit_std_input.setObjectName(u"logit_std_input")
        self.logit_std_input.setDecimals(4)
        self.logit_std_input.setSingleStep(0.010000000000000)
        self.logit_std_input.setValue(1.000000000000000)

        self.horizontalLayout_14.addWidget(self.logit_std_input)

        self.label_10 = QLabel(self.flux_training_box)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_14.addWidget(self.label_10)

        self.mode_scale_input = DoubleSpinBox(self.flux_training_box)
        self.mode_scale_input.setObjectName(u"mode_scale_input")
        self.mode_scale_input.setDecimals(4)
        self.mode_scale_input.setSingleStep(0.010000000000000)
        self.mode_scale_input.setValue(1.290000000000000)

        self.horizontalLayout_14.addWidget(self.mode_scale_input)


        self.formLayout_3.setLayout(5, QFormLayout.SpanningRole, self.horizontalLayout_14)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_11 = QLabel(self.flux_training_box)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_13.addWidget(self.label_11)

        self.sigmoid_scale_input = DoubleSpinBox(self.flux_training_box)
        self.sigmoid_scale_input.setObjectName(u"sigmoid_scale_input")
        self.sigmoid_scale_input.setDecimals(4)
        self.sigmoid_scale_input.setSingleStep(0.010000000000000)
        self.sigmoid_scale_input.setValue(1.000000000000000)

        self.horizontalLayout_13.addWidget(self.sigmoid_scale_input)

        self.label_7 = QLabel(self.flux_training_box)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_13.addWidget(self.label_7)

        self.discrete_flow_shift_input = DoubleSpinBox(self.flux_training_box)
        self.discrete_flow_shift_input.setObjectName(u"discrete_flow_shift_input")
        self.discrete_flow_shift_input.setDecimals(4)
        self.discrete_flow_shift_input.setSingleStep(0.010000000000000)
        self.discrete_flow_shift_input.setValue(1.150000000000000)

        self.horizontalLayout_13.addWidget(self.discrete_flow_shift_input)


        self.formLayout_3.setLayout(6, QFormLayout.SpanningRole, self.horizontalLayout_13)

        self.split_qkv_enable = QCheckBox(self.flux_training_box)
        self.split_qkv_enable.setObjectName(u"split_qkv_enable")
        sizePolicy.setHeightForWidth(self.split_qkv_enable.sizePolicy().hasHeightForWidth())
        self.split_qkv_enable.setSizePolicy(sizePolicy)

        self.formLayout_3.setWidget(7, QFormLayout.LabelRole, self.split_qkv_enable)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_13 = QLabel(self.flux_training_box)
        self.label_13.setObjectName(u"label_13")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.label_13)

        self.model_prediction_type_selector = ComboBox(self.flux_training_box)
        self.model_prediction_type_selector.addItem("")
        self.model_prediction_type_selector.addItem("")
        self.model_prediction_type_selector.addItem("")
        self.model_prediction_type_selector.setObjectName(u"model_prediction_type_selector")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.model_prediction_type_selector.sizePolicy().hasHeightForWidth())
        self.model_prediction_type_selector.setSizePolicy(sizePolicy3)

        self.horizontalLayout_6.addWidget(self.model_prediction_type_selector)

        self.blocks_to_swap_enable = QCheckBox(self.flux_training_box)
        self.blocks_to_swap_enable.setObjectName(u"blocks_to_swap_enable")

        self.horizontalLayout_6.addWidget(self.blocks_to_swap_enable)

        self.blocks_to_swap_input = SpinBox(self.flux_training_box)
        self.blocks_to_swap_input.setObjectName(u"blocks_to_swap_input")

        self.horizontalLayout_6.addWidget(self.blocks_to_swap_input)


        self.formLayout_3.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout_6)


        self.gridLayout_2.addLayout(self.formLayout_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.flux_training_box, 0, 0, 1, 1)


        self.retranslateUi(flux_ui)

        QMetaObject.connectSlotsByName(flux_ui)
    # setupUi

    def retranslateUi(self, flux_ui):
        flux_ui.setWindowTitle(QCoreApplication.translate("flux_ui", u"Form", None))
        self.flux_training_box.setTitle(QCoreApplication.translate("flux_ui", u"Train Flux", None))
        self.label.setText(QCoreApplication.translate("flux_ui", u"Ae Model", None))
        self.ae_model_selector.setText("")
        self.label_2.setText(QCoreApplication.translate("flux_ui", u"Clip L Model", None))
        self.clip_l_model_selector.setText("")
        self.label_3.setText(QCoreApplication.translate("flux_ui", u"T5 Model", None))
        self.t5_model_selector.setText("")
        self.apply_t5_attention_mask_enable.setText(QCoreApplication.translate("flux_ui", u"T5 Attention Mask", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("flux_ui", u"<html><head/><body><p>Max T5 Token Length represents the largest size a training prompt can be. Note that tokens are not the same as words. This is only for Flux training, 512 is default for dev, and 256 is default for schnell</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("flux_ui", u"T5 Max Length", None))
#if QT_CONFIG(tooltip)
        self.t5_max_token_input.setToolTip(QCoreApplication.translate("flux_ui", u"<html><head/><body><p>Max T5 Token Length represents the largest size a training prompt can be. Note that tokens are not the same as words. This is only for Flux training, 512 is default for dev, and 256 is default for schnell</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_12.setText(QCoreApplication.translate("flux_ui", u"Guidance Scale", None))
        self.split_mode_enable.setText(QCoreApplication.translate("flux_ui", u"Split Mode", None))
        self.label_6.setText(QCoreApplication.translate("flux_ui", u"Timestep Sampling", None))
        self.timestep_sampling_selector.setItemText(0, QCoreApplication.translate("flux_ui", u"Sigmoid", None))
        self.timestep_sampling_selector.setItemText(1, QCoreApplication.translate("flux_ui", u"Sigma", None))
        self.timestep_sampling_selector.setItemText(2, QCoreApplication.translate("flux_ui", u"Uniform", None))
        self.timestep_sampling_selector.setItemText(3, QCoreApplication.translate("flux_ui", u"Shift", None))
        self.timestep_sampling_selector.setItemText(4, QCoreApplication.translate("flux_ui", u"Flux Shift", None))

        self.label_5.setText(QCoreApplication.translate("flux_ui", u"Weighting Scheme", None))
        self.weighting_scheme_selector.setItemText(0, QCoreApplication.translate("flux_ui", u"None", None))
        self.weighting_scheme_selector.setItemText(1, QCoreApplication.translate("flux_ui", u"Sigma Sqrt", None))
        self.weighting_scheme_selector.setItemText(2, QCoreApplication.translate("flux_ui", u"Logit Normal", None))
        self.weighting_scheme_selector.setItemText(3, QCoreApplication.translate("flux_ui", u"Mode", None))
        self.weighting_scheme_selector.setItemText(4, QCoreApplication.translate("flux_ui", u"Cosmap", None))

        self.label_8.setText(QCoreApplication.translate("flux_ui", u"Logit mean", None))
        self.label_9.setText(QCoreApplication.translate("flux_ui", u"Logit std", None))
        self.label_10.setText(QCoreApplication.translate("flux_ui", u"Mode Scale", None))
        self.label_11.setText(QCoreApplication.translate("flux_ui", u"Sigmoid Scale", None))
        self.label_7.setText(QCoreApplication.translate("flux_ui", u"Discrete Flow Shift", None))
        self.split_qkv_enable.setText(QCoreApplication.translate("flux_ui", u"Split QKV", None))
        self.label_13.setText(QCoreApplication.translate("flux_ui", u"Model Pred Type", None))
        self.model_prediction_type_selector.setItemText(0, QCoreApplication.translate("flux_ui", u"Raw", None))
        self.model_prediction_type_selector.setItemText(1, QCoreApplication.translate("flux_ui", u"Sigma Scaled", None))
        self.model_prediction_type_selector.setItemText(2, QCoreApplication.translate("flux_ui", u"Additive", None))

        self.blocks_to_swap_enable.setText(QCoreApplication.translate("flux_ui", u"Blocks To Swap", None))
    # retranslateUi

