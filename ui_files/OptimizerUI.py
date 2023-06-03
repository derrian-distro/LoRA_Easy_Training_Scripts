# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OptimizerUI.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QLabel,
    QSizePolicy, QWidget)

from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox)

class Ui_optimizer_ui(object):
    def setupUi(self, optimizer_ui):
        if not optimizer_ui.objectName():
            optimizer_ui.setObjectName(u"optimizer_ui")
        optimizer_ui.resize(400, 317)
        self.formLayout = QFormLayout(optimizer_ui)
        self.formLayout.setObjectName(u"formLayout")
        self.optimizer_type_selector = ComboBox(optimizer_ui)
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

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.optimizer_type_selector)

        self.lr_scheduler_selector = ComboBox(optimizer_ui)
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.addItem("")
        self.lr_scheduler_selector.setObjectName(u"lr_scheduler_selector")
        self.lr_scheduler_selector.setFocusPolicy(Qt.StrongFocus)

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.lr_scheduler_selector)

        self.label = QLabel(optimizer_ui)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label)

        self.main_lr_input = LineEditWithHighlight(optimizer_ui)
        self.main_lr_input.setObjectName(u"main_lr_input")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.main_lr_input)

        self.unet_lr_enable = QCheckBox(optimizer_ui)
        self.unet_lr_enable.setObjectName(u"unet_lr_enable")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.unet_lr_enable)

        self.unet_lr_input = LineEditWithHighlight(optimizer_ui)
        self.unet_lr_input.setObjectName(u"unet_lr_input")
        self.unet_lr_input.setEnabled(False)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.unet_lr_input)

        self.te_lr_enable = QCheckBox(optimizer_ui)
        self.te_lr_enable.setObjectName(u"te_lr_enable")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.te_lr_enable)

        self.te_lr_input = LineEditWithHighlight(optimizer_ui)
        self.te_lr_input.setObjectName(u"te_lr_input")
        self.te_lr_input.setEnabled(False)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.te_lr_input)

        self.warmup_enable = QCheckBox(optimizer_ui)
        self.warmup_enable.setObjectName(u"warmup_enable")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.warmup_enable)

        self.warmup_ratio_input = DoubleSpinBox(optimizer_ui)
        self.warmup_ratio_input.setObjectName(u"warmup_ratio_input")
        self.warmup_ratio_input.setEnabled(False)
        self.warmup_ratio_input.setFocusPolicy(Qt.StrongFocus)
        self.warmup_ratio_input.setMaximum(1.000000000000000)
        self.warmup_ratio_input.setSingleStep(0.010000000000000)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.warmup_ratio_input)

        self.label_4 = QLabel(optimizer_ui)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_4)

        self.cosine_restart_input = SpinBox(optimizer_ui)
        self.cosine_restart_input.setObjectName(u"cosine_restart_input")
        self.cosine_restart_input.setEnabled(False)
        self.cosine_restart_input.setFocusPolicy(Qt.StrongFocus)
        self.cosine_restart_input.setMinimum(1)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.cosine_restart_input)

        self.label_5 = QLabel(optimizer_ui)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_5)

        self.poly_power_input = DoubleSpinBox(optimizer_ui)
        self.poly_power_input.setObjectName(u"poly_power_input")
        self.poly_power_input.setEnabled(False)
        self.poly_power_input.setFocusPolicy(Qt.StrongFocus)
        self.poly_power_input.setSingleStep(0.010000000000000)
        self.poly_power_input.setValue(1.000000000000000)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.poly_power_input)

        self.min_snr_enable = QCheckBox(optimizer_ui)
        self.min_snr_enable.setObjectName(u"min_snr_enable")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.min_snr_enable)

        self.min_snr_input = SpinBox(optimizer_ui)
        self.min_snr_input.setObjectName(u"min_snr_input")
        self.min_snr_input.setEnabled(False)
        self.min_snr_input.setFocusPolicy(Qt.StrongFocus)
        self.min_snr_input.setValue(5)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.min_snr_input)

        self.scale_weight_enable = QCheckBox(optimizer_ui)
        self.scale_weight_enable.setObjectName(u"scale_weight_enable")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.scale_weight_enable)

        self.scale_weight_input = DoubleSpinBox(optimizer_ui)
        self.scale_weight_input.setObjectName(u"scale_weight_input")
        self.scale_weight_input.setEnabled(False)
        self.scale_weight_input.setFocusPolicy(Qt.StrongFocus)
        self.scale_weight_input.setValue(1.000000000000000)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.scale_weight_input)


        self.retranslateUi(optimizer_ui)

        QMetaObject.connectSlotsByName(optimizer_ui)
    # setupUi

    def retranslateUi(self, optimizer_ui):
        optimizer_ui.setWindowTitle(QCoreApplication.translate("optimizer_ui", u"Form", None))
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

#if QT_CONFIG(tooltip)
        self.optimizer_type_selector.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The optimizer to use, The standard, and the one most people use is AdamW8bit.</p><p>The various Dadapt modify the lr on their own as you go, however can only take one lr.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lr_scheduler_selector.setItemText(0, QCoreApplication.translate("optimizer_ui", u"cosine", None))
        self.lr_scheduler_selector.setItemText(1, QCoreApplication.translate("optimizer_ui", u"cosine with restarts", None))
        self.lr_scheduler_selector.setItemText(2, QCoreApplication.translate("optimizer_ui", u"linear", None))
        self.lr_scheduler_selector.setItemText(3, QCoreApplication.translate("optimizer_ui", u"constant", None))
        self.lr_scheduler_selector.setItemText(4, QCoreApplication.translate("optimizer_ui", u"constant with warmup", None))
        self.lr_scheduler_selector.setItemText(5, QCoreApplication.translate("optimizer_ui", u"adafactor", None))
        self.lr_scheduler_selector.setItemText(6, QCoreApplication.translate("optimizer_ui", u"polynomial", None))

#if QT_CONFIG(tooltip)
        self.lr_scheduler_selector.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The scheduler for the lr. The ones I use personally are cosine and cosine with restarts.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("optimizer_ui", u"Learning Rate", None))
#if QT_CONFIG(tooltip)
        self.main_lr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The main lr. If you have both unet and te set though it is just completely overwritten.</p><p>note that if you don't put in a proper number, it will just be read as 0.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.main_lr_input.setText(QCoreApplication.translate("optimizer_ui", u"1e-4", None))
        self.main_lr_input.setPlaceholderText(QCoreApplication.translate("optimizer_ui", u"Learning Rate", None))
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
        self.warmup_enable.setText(QCoreApplication.translate("optimizer_ui", u"Warmup Ratio", None))
#if QT_CONFIG(tooltip)
        self.warmup_ratio_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>This is ratio of steps you want to be a warmup to your chosen lr. I personally use 0.05 (5%).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("optimizer_ui", u"Num Restarts", None))
#if QT_CONFIG(tooltip)
        self.cosine_restart_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The number of times cosine with restarts will restart, note that 1 means it doesn't restart, and 2 means it will restart once.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("optimizer_ui", u"Polynomial Power", None))
#if QT_CONFIG(tooltip)
        self.poly_power_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>The power of the polynomial equation. The closer to 0 the more agressive (I think).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.min_snr_enable.setText(QCoreApplication.translate("optimizer_ui", u"Minimum SNR Gamma", None))
#if QT_CONFIG(tooltip)
        self.min_snr_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>This is a tool that reduces learning of unwanted elements by only learning what is the most common. This can lead to it not learning small details however. The recommended value is 5. Lower values apply more.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.scale_weight_enable.setText(QCoreApplication.translate("optimizer_ui", u"Scale Weight Normals", None))
#if QT_CONFIG(tooltip)
        self.scale_weight_input.setToolTip(QCoreApplication.translate("optimizer_ui", u"<html><head/><body><p>An implementation of the idea of max norm regularization. Basically, this will help stabilize network training by limiting the normal of network weights. Might work well for limiting overfitting or baking.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

