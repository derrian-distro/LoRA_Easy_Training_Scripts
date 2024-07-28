# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OptimizerUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox, TabView)

class Ui_optimizer_ui(object):
    def setupUi(self, optimizer_ui):
        if not optimizer_ui.objectName():
            optimizer_ui.setObjectName(u"optimizer_ui")
        optimizer_ui.resize(463, 354)
        self.verticalLayout = QVBoxLayout(optimizer_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = TabView(optimizer_ui)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setFocusPolicy(Qt.StrongFocus)
        self.optimizer_tab_main = QWidget()
        self.optimizer_tab_main.setObjectName(u"optimizer_tab_main")
        self.optimizer_tab_main.setFocusPolicy(Qt.StrongFocus)
        self.gridLayout = QGridLayout(self.optimizer_tab_main)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(self.optimizer_tab_main)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.main_lr_input = LineEditWithHighlight(self.optimizer_tab_main)
        self.main_lr_input.setObjectName(u"main_lr_input")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.main_lr_input)

        self.min_lr_input = LineEditWithHighlight(self.optimizer_tab_main)
        self.min_lr_input.setObjectName(u"min_lr_input")
        self.min_lr_input.setEnabled(False)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.min_lr_input)

        self.unet_lr_enable = QCheckBox(self.optimizer_tab_main)
        self.unet_lr_enable.setObjectName(u"unet_lr_enable")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.unet_lr_enable)

        self.unet_lr_input = LineEditWithHighlight(self.optimizer_tab_main)
        self.unet_lr_input.setObjectName(u"unet_lr_input")
        self.unet_lr_input.setEnabled(False)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.unet_lr_input)

        self.te_lr_enable = QCheckBox(self.optimizer_tab_main)
        self.te_lr_enable.setObjectName(u"te_lr_enable")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.te_lr_enable)

        self.te_lr_input = LineEditWithHighlight(self.optimizer_tab_main)
        self.te_lr_input.setObjectName(u"te_lr_input")
        self.te_lr_input.setEnabled(False)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.te_lr_input)

        self.min_lr_label = QLabel(self.optimizer_tab_main)
        self.min_lr_label.setObjectName(u"min_lr_label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.min_lr_label)

        self.scale_weight_enable = QCheckBox(self.optimizer_tab_main)
        self.scale_weight_enable.setObjectName(u"scale_weight_enable")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.scale_weight_enable)

        self.scale_weight_input = DoubleSpinBox(self.optimizer_tab_main)
        self.scale_weight_input.setObjectName(u"scale_weight_input")
        self.scale_weight_input.setEnabled(False)
        self.scale_weight_input.setFocusPolicy(Qt.StrongFocus)
        self.scale_weight_input.setValue(1.000000000000000)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.scale_weight_input)

        self.min_snr_enable = QCheckBox(self.optimizer_tab_main)
        self.min_snr_enable.setObjectName(u"min_snr_enable")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.min_snr_enable)

        self.min_snr_input = SpinBox(self.optimizer_tab_main)
        self.min_snr_input.setObjectName(u"min_snr_input")
        self.min_snr_input.setEnabled(False)
        self.min_snr_input.setFocusPolicy(Qt.StrongFocus)
        self.min_snr_input.setValue(5)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.min_snr_input)

        self.huber_schedule_selector = ComboBox(self.optimizer_tab_main)
        self.huber_schedule_selector.addItem("")
        self.huber_schedule_selector.addItem("")
        self.huber_schedule_selector.addItem("")
        self.huber_schedule_selector.setObjectName(u"huber_schedule_selector")
        self.huber_schedule_selector.setEnabled(False)

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.huber_schedule_selector)

        self.label_3 = QLabel(self.optimizer_tab_main)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_3)


        self.gridLayout.addLayout(self.formLayout_2, 1, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.optimizer_type_label = QLabel(self.optimizer_tab_main)
        self.optimizer_type_label.setObjectName(u"optimizer_type_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.optimizer_type_label)

        self.optimizer_type_selector = ComboBox(self.optimizer_tab_main)
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.addItem("")
        self.optimizer_type_selector.setObjectName(u"optimizer_type_selector")
        self.optimizer_type_selector.setFocusPolicy(Qt.StrongFocus)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.optimizer_type_selector)

        self.lr_scheduler_label = QLabel(self.optimizer_tab_main)
        self.lr_scheduler_label.setObjectName(u"lr_scheduler_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lr_scheduler_label)

        self.lr_scheduler_selector = ComboBox(self.optimizer_tab_main)
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.setObjectName(u"lr_scheduler_selector")
        self.lr_scheduler_selector.setFocusPolicy(Qt.StrongFocus)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lr_scheduler_selector)

        self.loss_type_label = QLabel(self.optimizer_tab_main)
        self.loss_type_label.setObjectName(u"loss_type_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.loss_type_label)

        self.loss_type_selector = ComboBox(self.optimizer_tab_main)
        self.loss_type_selector.addItem("")
        self.loss_type_selector.addItem("")
        self.loss_type_selector.addItem("")
        self.loss_type_selector.setObjectName(u"loss_type_selector")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.loss_type_selector)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 2)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.warmup_enable = QCheckBox(self.optimizer_tab_main)
        self.warmup_enable.setObjectName(u"warmup_enable")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.warmup_enable)

        self.warmup_input = DoubleSpinBox(self.optimizer_tab_main)
        self.warmup_input.setObjectName(u"warmup_input")
        self.warmup_input.setEnabled(False)
        self.warmup_input.setFocusPolicy(Qt.StrongFocus)
        self.warmup_input.setMaximum(1.000000000000000)
        self.warmup_input.setSingleStep(0.010000000000000)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.warmup_input)

        self.label_4 = QLabel(self.optimizer_tab_main)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.cosine_restart_input = SpinBox(self.optimizer_tab_main)
        self.cosine_restart_input.setObjectName(u"cosine_restart_input")
        self.cosine_restart_input.setEnabled(False)
        self.cosine_restart_input.setFocusPolicy(Qt.StrongFocus)
        self.cosine_restart_input.setMinimum(1)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.cosine_restart_input)

        self.label_5 = QLabel(self.optimizer_tab_main)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.poly_power_input = DoubleSpinBox(self.optimizer_tab_main)
        self.poly_power_input.setObjectName(u"poly_power_input")
        self.poly_power_input.setEnabled(False)
        self.poly_power_input.setFocusPolicy(Qt.StrongFocus)
        self.poly_power_input.setSingleStep(0.010000000000000)
        self.poly_power_input.setValue(1.000000000000000)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.poly_power_input)

        self.gamma_label = QLabel(self.optimizer_tab_main)
        self.gamma_label.setObjectName(u"gamma_label")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.gamma_label)

        self.gamma_input = DoubleSpinBox(self.optimizer_tab_main)
        self.gamma_input.setObjectName(u"gamma_input")
        self.gamma_input.setEnabled(False)
        self.gamma_input.setMinimum(0.000000000000000)
        self.gamma_input.setMaximum(1.000000000000000)
        self.gamma_input.setSingleStep(0.010000000000000)
        self.gamma_input.setValue(0.100000000000000)

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.gamma_input)

        self.max_grad_norm_input = DoubleSpinBox(self.optimizer_tab_main)
        self.max_grad_norm_input.setObjectName(u"max_grad_norm_input")
        self.max_grad_norm_input.setValue(1.000000000000000)

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.max_grad_norm_input)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.zero_term_enable = QCheckBox(self.optimizer_tab_main)
        self.zero_term_enable.setObjectName(u"zero_term_enable")

        self.horizontalLayout_2.addWidget(self.zero_term_enable)

        self.masked_loss_enable = QCheckBox(self.optimizer_tab_main)
        self.masked_loss_enable.setObjectName(u"masked_loss_enable")

        self.horizontalLayout_2.addWidget(self.masked_loss_enable)


        self.formLayout_3.setLayout(5, QFormLayout.SpanningRole, self.horizontalLayout_2)

        self.label_6 = QLabel(self.optimizer_tab_main)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_3.setWidget(6, QFormLayout.LabelRole, self.label_6)

        self.huber_param_input = DoubleSpinBox(self.optimizer_tab_main)
        self.huber_param_input.setObjectName(u"huber_param_input")
        self.huber_param_input.setEnabled(False)
        self.huber_param_input.setDecimals(4)
        self.huber_param_input.setSingleStep(0.010000000000000)
        self.huber_param_input.setValue(0.100000000000000)

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.huber_param_input)

        self.label_2 = QLabel(self.optimizer_tab_main)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_2)


        self.gridLayout.addLayout(self.formLayout_3, 1, 1, 1, 1)

        self.tabWidget.addTab(self.optimizer_tab_main, "")
        self.optimizer_tab_args = QWidget()
        self.optimizer_tab_args.setObjectName(u"optimizer_tab_args")
        self.optimizer_tab_args.setFocusPolicy(Qt.StrongFocus)
        self.verticalLayout_2 = QVBoxLayout(self.optimizer_tab_args)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.add_opt_button = QPushButton(self.optimizer_tab_args)
        self.add_opt_button.setObjectName(u"add_opt_button")

        self.verticalLayout_2.addWidget(self.add_opt_button)

        self.scrollArea = QScrollArea(self.optimizer_tab_args)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.optimizer_item_widget = QWidget()
        self.optimizer_item_widget.setObjectName(u"optimizer_item_widget")
        self.optimizer_item_widget.setGeometry(QRect(0, 0, 439, 274))
        self.verticalLayout_3 = QVBoxLayout(self.optimizer_item_widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea.setWidget(self.optimizer_item_widget)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.optimizer_tab_args, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(optimizer_ui)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(optimizer_ui)
    # setupUi

    def retranslateUi(self, optimizer_ui):
        optimizer_ui.setWindowTitle(QCoreApplication.translate("optimizer_ui", u"Form", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Learning Rate is the base learning rate for any value that is not explicitly set, for example, if you set the Unet learning rate, but not the Text Encoder learning rate, the Text Encoder will be using this learning rate</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("optimizer_ui", u"Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.main_lr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Learning Rate is the base learning rate for any value that is not explicitly set, for example, if you set the Unet learning rate, but not the Text Encoder learning rate, the Text Encoder will be using this learning rate</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.main_lr_input.setText(QCoreApplication.translate("optimizer_ui", u"1e-4", None))
        self.main_lr_input.setPlaceholderText(QCoreApplication.translate("optimizer_ui", u"Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.min_lr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Minimum Learning Rate is the minimum value any of the learning rates can be</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.min_lr_input.setText(QCoreApplication.translate("optimizer_ui", u"1e-6", None))
#if QT_CONFIG(tooltip)
        self.unet_lr_enable.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Unet Learning Rate is the base learning rate for the Unet</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.unet_lr_enable.setText(QCoreApplication.translate("optimizer_ui", u"Unet Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.unet_lr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Unet Learning Rate is the base learning rate for the Unet</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.unet_lr_input.setText(QCoreApplication.translate("optimizer_ui", u"1e-4", None))
        self.unet_lr_input.setPlaceholderText(QCoreApplication.translate("optimizer_ui", u"Unet Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.te_lr_enable.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>TE Learning Rate is the base learning rate for the Text Encoder</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.te_lr_enable.setText(QCoreApplication.translate("optimizer_ui", u"TE Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.te_lr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>TE Learning Rate is the base learning rate for the Text Encoder</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.te_lr_input.setText(QCoreApplication.translate("optimizer_ui", u"1e-4", None))
        self.te_lr_input.setPlaceholderText(QCoreApplication.translate("optimizer_ui", u"TE Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.min_lr_label.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Minimum Learning Rate is the minimum value any of the learning rates can be</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.min_lr_label.setText(QCoreApplication.translate("optimizer_ui", u"Minimum Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.scale_weight_enable.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Scale Weight Norms is a way to scale the weights to prevent any one weight from getting too large to the rest</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.scale_weight_enable.setText(QCoreApplication.translate("optimizer_ui", u"Scale Weight Norms", None))
#if QT_CONFIG(tooltip)
        self.scale_weight_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Scale Weight Norms is a way to scale the weights to prevent any one weight from getting too large to the rest</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.min_snr_enable.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Min SNR Gamma is a way to remove random noise during training. A lower value is stronger</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.min_snr_enable.setText(QCoreApplication.translate("optimizer_ui", u"Min SNR Gamma", None))
#if QT_CONFIG(tooltip)
        self.min_snr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Min SNR Gamma is a way to remove random noise during training. A lower value is stronger</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.huber_schedule_selector.setItemText(0, QCoreApplication.translate("optimizer_ui", u"SNR", None))
        self.huber_schedule_selector.setItemText(1, QCoreApplication.translate("optimizer_ui", u"Exponential", None))
        self.huber_schedule_selector.setItemText(2, QCoreApplication.translate("optimizer_ui", u"Constant", None))

#if QT_CONFIG(tooltip)
        self.huber_schedule_selector.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Huber Schedule handles the type of Huber loss that is used.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Huber Schedule handles the type of Huber loss that is used.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("optimizer_ui", u"Huber Schedule", None))
#if QT_CONFIG(tooltip)
        self.optimizer_type_label.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Optimizer Type is the Optimizer that will be used during training</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.optimizer_type_label.setText(QCoreApplication.translate("optimizer_ui", u"Optimizer Type", None))
        self.optimizer_type_selector.setItemText(0, QCoreApplication.translate("optimizer_ui", u"AdamW", None))
        self.optimizer_type_selector.setItemText(1, QCoreApplication.translate("optimizer_ui", u"AdamW8bit", None))
        self.optimizer_type_selector.setItemText(2, QCoreApplication.translate("optimizer_ui", u"Lion", None))
        self.optimizer_type_selector.setItemText(3, QCoreApplication.translate("optimizer_ui", u"SGDNesterov", None))
        self.optimizer_type_selector.setItemText(4, QCoreApplication.translate("optimizer_ui", u"SGDNesterov8bit", None))
        self.optimizer_type_selector.setItemText(5, QCoreApplication.translate("optimizer_ui", u"DAdaptAdam", None))
        self.optimizer_type_selector.setItemText(6, QCoreApplication.translate("optimizer_ui", u"DAdaptAdaGrad", None))
        self.optimizer_type_selector.setItemText(7, QCoreApplication.translate("optimizer_ui", u"DAdaptAdan", None))
        self.optimizer_type_selector.setItemText(8, QCoreApplication.translate("optimizer_ui", u"DAdaptSGD", None))
        self.optimizer_type_selector.setItemText(9, QCoreApplication.translate("optimizer_ui", u"AdaFactor", None))
        self.optimizer_type_selector.setItemText(10, QCoreApplication.translate("optimizer_ui", u"Prodigy", None))
        self.optimizer_type_selector.setItemText(11, QCoreApplication.translate("optimizer_ui", u"Came", None))

#if QT_CONFIG(tooltip)
        self.optimizer_type_selector.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Optimizer Type is the Optimizer that will be used during training</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lr_scheduler_label.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>LR Scheduler is the Scheduler for the learning rate during the training</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lr_scheduler_label.setText(QCoreApplication.translate("optimizer_ui", u"LR Scheduler", None))
        self.lr_scheduler_selector.setItemText(0, QCoreApplication.translate("optimizer_ui", u"cosine", None))
        self.lr_scheduler_selector.setItemText(1, QCoreApplication.translate("optimizer_ui", u"cosine with restarts", None))
        self.lr_scheduler_selector.setItemText(2, QCoreApplication.translate("optimizer_ui", u"cosine annealing warm restarts (CAWR)", None))
        self.lr_scheduler_selector.setItemText(3, QCoreApplication.translate("optimizer_ui", u"linear", None))
        self.lr_scheduler_selector.setItemText(4, QCoreApplication.translate("optimizer_ui", u"constant", None))
        self.lr_scheduler_selector.setItemText(5, QCoreApplication.translate("optimizer_ui", u"constant with warmup", None))
        self.lr_scheduler_selector.setItemText(6, QCoreApplication.translate("optimizer_ui", u"adafactor", None))
        self.lr_scheduler_selector.setItemText(7, QCoreApplication.translate("optimizer_ui", u"polynomial", None))
        self.lr_scheduler_selector.setItemText(8, QCoreApplication.translate("optimizer_ui", u"rex annealing warm restarts (RAWR)", None))

#if QT_CONFIG(tooltip)
        self.lr_scheduler_selector.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>LR Scheduler is the Scheduler for the learning rate during the training</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.loss_type_label.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Loss Type is the way the loss is calculated</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.loss_type_label.setText(QCoreApplication.translate("optimizer_ui", u"Loss Type", None))
        self.loss_type_selector.setItemText(0, QCoreApplication.translate("optimizer_ui", u"L2", None))
        self.loss_type_selector.setItemText(1, QCoreApplication.translate("optimizer_ui", u"Huber", None))
        self.loss_type_selector.setItemText(2, QCoreApplication.translate("optimizer_ui", u"Smooth L1", None))

#if QT_CONFIG(tooltip)
        self.loss_type_selector.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Loss Type is the way the loss is calculated</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.warmup_enable.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Warmup Ratio is the ratio of steps that is warmup steps in comparison to the total number of steps. If you are using one of the &quot;warm&quot; schedulers, the warmup is spread evenly across each of the cycles</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.warmup_enable.setText(QCoreApplication.translate("optimizer_ui", u"Warmup Ratio", None))
#if QT_CONFIG(tooltip)
        self.warmup_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Warmup Ratio is the ratio of steps that is warmup steps in comparison to the total number of steps. If you are using one of the &quot;warm&quot; schedulers, the warmup is spread evenly across each of the cycles</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Number of Cycles. 1 means there won't be any restarts during the training</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("optimizer_ui", u"Num Cycles", None))
#if QT_CONFIG(tooltip)
        self.cosine_restart_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Number of Cycles. 1 means there won't be any restarts during the training</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Polynomial Power is the value of the Polynomial for the Polynomial Scheduler</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("optimizer_ui", u"Polynomial Power", None))
#if QT_CONFIG(tooltip)
        self.poly_power_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Polynomial Power is the value of the Polynomial for the Polynomial Scheduler</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.gamma_label.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Restart Decay is the amount the max learning rate decays when a new cycle starts</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.gamma_label.setText(QCoreApplication.translate("optimizer_ui", u"Restart Decay", None))
#if QT_CONFIG(tooltip)
        self.gamma_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Restart Decay is the amount the max learning rate decays when a new cycle starts</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.max_grad_norm_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Max Grad Norm is the maximum gradient after normalization</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.zero_term_enable.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Zero Term SNR is a tweak to the noise schedule that allows for full range of color. Typically you would only use this if the base model you are training on has trained with it</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.zero_term_enable.setText(QCoreApplication.translate("optimizer_ui", u"Zero Term SNR", None))
#if QT_CONFIG(tooltip)
        self.masked_loss_enable.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Masked loss activates the masking feature of sd-scripts. This type of loss will only calculate the loss according to the masked values in the training images</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.masked_loss_enable.setText(QCoreApplication.translate("optimizer_ui", u"Masked Loss", None))
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Huber Param is a parameter that affects the calculation of the loss function</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("optimizer_ui", u"Huber Param", None))
#if QT_CONFIG(tooltip)
        self.huber_param_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Huber Param is a parameter that affects the calculation of the loss function</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>Max Grad Norm is the maximum gradient after normalization</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("optimizer_ui", u"Max Grad Norm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optimizer_tab_main), QCoreApplication.translate("optimizer_ui", u"Main Args", None))
        self.add_opt_button.setText(QCoreApplication.translate("optimizer_ui", u"Add Optimizer Arg", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optimizer_tab_args), QCoreApplication.translate("optimizer_ui", u"Optional Args", None))
    # retranslateUi

