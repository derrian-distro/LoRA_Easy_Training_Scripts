# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OptimizerUI.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGridLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox, TabView)

class Ui_optimizer_ui(object):
    def setupUi(self, optimizer_ui):
        if not optimizer_ui.objectName():
            optimizer_ui.setObjectName(u"optimizer_ui")
        optimizer_ui.resize(421, 350)
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

        self.label_2 = QLabel(self.optimizer_tab_main)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_2)

        self.max_grad_norm_input = DoubleSpinBox(self.optimizer_tab_main)
        self.max_grad_norm_input.setObjectName(u"max_grad_norm_input")
        self.max_grad_norm_input.setValue(1.000000000000000)

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.max_grad_norm_input)

        self.zero_term_enable = QCheckBox(self.optimizer_tab_main)
        self.zero_term_enable.setObjectName(u"zero_term_enable")

        self.formLayout_3.setWidget(5, QFormLayout.SpanningRole, self.zero_term_enable)

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
        self.optimizer_item_widget.setGeometry(QRect(0, 0, 363, 233))
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
        self.label.setText(QCoreApplication.translate("optimizer_ui", u"Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.main_lr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The main lr. If you have both unet and te set though it is just completely overwritten.</p><p>note that if you don't put in a proper number, it will just be read as 0.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.main_lr_input.setText(QCoreApplication.translate("optimizer_ui", u"1e-4", None))
        self.main_lr_input.setPlaceholderText(QCoreApplication.translate("optimizer_ui", u"Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.min_lr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The minimum lr for the Cosine Annealing Warmup Restarts LR scheduler. This is the final lr before a restart occurs.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.min_lr_input.setText(QCoreApplication.translate("optimizer_ui", u"1e-6", None))
        self.unet_lr_enable.setText(QCoreApplication.translate("optimizer_ui", u"Unet Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.unet_lr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The Unet lr. Overrides the base lr, if you don't have a proper number set, it will be 0</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.unet_lr_input.setText(QCoreApplication.translate("optimizer_ui", u"1e-4", None))
        self.unet_lr_input.setPlaceholderText(QCoreApplication.translate("optimizer_ui", u"Unet Learning Rate", None))
        self.te_lr_enable.setText(QCoreApplication.translate("optimizer_ui", u"TE Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.te_lr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The Text Encoder lr. Overrides the base lr, if you don't have a proper number set, it will be 0</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.te_lr_input.setText(QCoreApplication.translate("optimizer_ui", u"1e-4", None))
        self.te_lr_input.setPlaceholderText(QCoreApplication.translate("optimizer_ui", u"TE Learning Rate", None))
        self.min_lr_label.setText(QCoreApplication.translate("optimizer_ui", u"Minimum Learning Rate", None))
        self.scale_weight_enable.setText(QCoreApplication.translate("optimizer_ui", u"Scale Weight Norms", None))
#if QT_CONFIG(tooltip)
        self.scale_weight_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>An implementation of the idea of max norm regularization. Basically, this will help stabilize network training by limiting the normal of network weights. Might work well for limiting overfitting or baking.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.min_snr_enable.setText(QCoreApplication.translate("optimizer_ui", u"Min SNR Gamma", None))
#if QT_CONFIG(tooltip)
        self.min_snr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>This is a tool that reduces learning of unwanted elements by only learning what is the most common. This can lead to it not learning small details however. The recommended value is 5. Lower values apply more.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.huber_schedule_selector.setItemText(0, QCoreApplication.translate("optimizer_ui", u"SNR", None))
        self.huber_schedule_selector.setItemText(1, QCoreApplication.translate("optimizer_ui", u"Exponential", None))
        self.huber_schedule_selector.setItemText(2, QCoreApplication.translate("optimizer_ui", u"Constant", None))

        self.label_3.setText(QCoreApplication.translate("optimizer_ui", u"Huber Schedule", None))
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
        self.optimizer_type_selector.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The optimizer to use, The standard, and the one most people use is AdamW8bit.</p><p>The various Dadapt modify the lr on their own as you go, however can only take one lr.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lr_scheduler_label.setText(QCoreApplication.translate("optimizer_ui", u"LR Scheduler", None))
        self.lr_scheduler_selector.setItemText(0, QCoreApplication.translate("optimizer_ui", u"cosine", None))
        self.lr_scheduler_selector.setItemText(1, QCoreApplication.translate("optimizer_ui", u"cosine with restarts", None))
        self.lr_scheduler_selector.setItemText(2, QCoreApplication.translate("optimizer_ui", u"cosine annealing warmup restarts", None))
        self.lr_scheduler_selector.setItemText(3, QCoreApplication.translate("optimizer_ui", u"linear", None))
        self.lr_scheduler_selector.setItemText(4, QCoreApplication.translate("optimizer_ui", u"constant", None))
        self.lr_scheduler_selector.setItemText(5, QCoreApplication.translate("optimizer_ui", u"constant with warmup", None))
        self.lr_scheduler_selector.setItemText(6, QCoreApplication.translate("optimizer_ui", u"adafactor", None))
        self.lr_scheduler_selector.setItemText(7, QCoreApplication.translate("optimizer_ui", u"polynomial", None))
        self.lr_scheduler_selector.setItemText(8, QCoreApplication.translate("optimizer_ui", u"rex", None))

#if QT_CONFIG(tooltip)
        self.lr_scheduler_selector.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The scheduler for the lr. The ones I use personally are cosine and cosine with restarts.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.loss_type_label.setText(QCoreApplication.translate("optimizer_ui", u"Loss Type", None))
        self.loss_type_selector.setItemText(0, QCoreApplication.translate("optimizer_ui", u"L2", None))
        self.loss_type_selector.setItemText(1, QCoreApplication.translate("optimizer_ui", u"Huber", None))
        self.loss_type_selector.setItemText(2, QCoreApplication.translate("optimizer_ui", u"Smooth L1", None))

        self.warmup_enable.setText(QCoreApplication.translate("optimizer_ui", u"Warmup Ratio", None))
#if QT_CONFIG(tooltip)
        self.warmup_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>This is ratio of steps you want to be a warmup to your chosen lr. I personally use 0.05 (5%). Keep in mind this is spread out over the course of all restarts when using the Cosine Annealing Warmup Restarts LR scheduler.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("optimizer_ui", u"Num Restarts", None))
#if QT_CONFIG(tooltip)
        self.cosine_restart_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The number of times cosine with restarts will restart, note that 1 means it doesn't restart, and 2 means it will restart once.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("optimizer_ui", u"Polynomial Power", None))
#if QT_CONFIG(tooltip)
        self.poly_power_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The power of the polynomial equation. The closer to 0 the more agressive (I think).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.gamma_label.setText(QCoreApplication.translate("optimizer_ui", u"Restart Decay", None))
#if QT_CONFIG(tooltip)
        self.gamma_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The percent that decays on restart. Unique to Cosine Annealing Warmup Restarts.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("optimizer_ui", u"Max Grad Norm", None))
        self.zero_term_enable.setText(QCoreApplication.translate("optimizer_ui", u"Zero Term SNR", None))
        self.label_6.setText(QCoreApplication.translate("optimizer_ui", u"Huber Param", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optimizer_tab_main), QCoreApplication.translate("optimizer_ui", u"Main Args", None))
        self.add_opt_button.setText(QCoreApplication.translate("optimizer_ui", u"Add Optimizer Arg", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optimizer_tab_args), QCoreApplication.translate("optimizer_ui", u"Optional Args", None))
    # retranslateUi

