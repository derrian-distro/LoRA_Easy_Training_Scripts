# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NetworkUI.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QSizePolicy,
    QWidget)

from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox)

class Ui_network_ui(object):
    def setupUi(self, network_ui):
        if not network_ui.objectName():
            network_ui.setObjectName(u"network_ui")
        network_ui.resize(400, 233)
        self.formLayout = QFormLayout(network_ui)
        self.formLayout.setObjectName(u"formLayout")
        self.algo_select = ComboBox(network_ui)
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.setObjectName(u"algo_select")
        self.algo_select.setFocusPolicy(Qt.StrongFocus)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.algo_select)

        self.network_dim_label = QLabel(network_ui)
        self.network_dim_label.setObjectName(u"network_dim_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.network_dim_label)

        self.network_dim_input = SpinBox(network_ui)
        self.network_dim_input.setObjectName(u"network_dim_input")
        self.network_dim_input.setFocusPolicy(Qt.StrongFocus)
        self.network_dim_input.setMinimum(1)
        self.network_dim_input.setMaximum(16777215)
        self.network_dim_input.setValue(32)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.network_dim_input)

        self.network_alpha_label = QLabel(network_ui)
        self.network_alpha_label.setObjectName(u"network_alpha_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.network_alpha_label)

        self.network_alpha_input = DoubleSpinBox(network_ui)
        self.network_alpha_input.setObjectName(u"network_alpha_input")
        self.network_alpha_input.setFocusPolicy(Qt.StrongFocus)
        self.network_alpha_input.setDecimals(2)
        self.network_alpha_input.setMaximum(16777215.000000000000000)
        self.network_alpha_input.setValue(16.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.network_alpha_input)

        self.unet_te_both_label = QLabel(network_ui)
        self.unet_te_both_label.setObjectName(u"unet_te_both_label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.unet_te_both_label)

        self.unet_te_both_select = ComboBox(network_ui)
        self.unet_te_both_select.addItem("")
        self.unet_te_both_select.addItem("")
        self.unet_te_both_select.addItem("")
        self.unet_te_both_select.setObjectName(u"unet_te_both_select")
        self.unet_te_both_select.setFocusPolicy(Qt.StrongFocus)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.unet_te_both_select)

        self.conv_dim_label = QLabel(network_ui)
        self.conv_dim_label.setObjectName(u"conv_dim_label")
        self.conv_dim_label.setEnabled(True)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.conv_dim_label)

        self.conv_dim_input = SpinBox(network_ui)
        self.conv_dim_input.setObjectName(u"conv_dim_input")
        self.conv_dim_input.setEnabled(False)
        self.conv_dim_input.setFocusPolicy(Qt.StrongFocus)
        self.conv_dim_input.setMaximum(16777215)
        self.conv_dim_input.setValue(32)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.conv_dim_input)

        self.conv_alpha_label = QLabel(network_ui)
        self.conv_alpha_label.setObjectName(u"conv_alpha_label")
        self.conv_alpha_label.setEnabled(True)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.conv_alpha_label)

        self.conv_alpha_input = DoubleSpinBox(network_ui)
        self.conv_alpha_input.setObjectName(u"conv_alpha_input")
        self.conv_alpha_input.setEnabled(False)
        self.conv_alpha_input.setFocusPolicy(Qt.StrongFocus)
        self.conv_alpha_input.setMaximum(16777215.000000000000000)
        self.conv_alpha_input.setValue(16.000000000000000)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.conv_alpha_input)

        self.dylora_unit_label = QLabel(network_ui)
        self.dylora_unit_label.setObjectName(u"dylora_unit_label")
        self.dylora_unit_label.setEnabled(True)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.dylora_unit_label)

        self.dylora_unit_input = SpinBox(network_ui)
        self.dylora_unit_input.setObjectName(u"dylora_unit_input")
        self.dylora_unit_input.setEnabled(False)
        self.dylora_unit_input.setFocusPolicy(Qt.StrongFocus)
        self.dylora_unit_input.setValue(4)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.dylora_unit_input)


        self.retranslateUi(network_ui)

        QMetaObject.connectSlotsByName(network_ui)
    # setupUi

    def retranslateUi(self, network_ui):
        network_ui.setWindowTitle(QCoreApplication.translate("network_ui", u"Form", None))
        self.algo_select.setItemText(0, QCoreApplication.translate("network_ui", u"LoRA", None))
        self.algo_select.setItemText(1, QCoreApplication.translate("network_ui", u"LoCon", None))
        self.algo_select.setItemText(2, QCoreApplication.translate("network_ui", u"LoHa", None))
        self.algo_select.setItemText(3, QCoreApplication.translate("network_ui", u"IA3", None))
        self.algo_select.setItemText(4, QCoreApplication.translate("network_ui", u"Lokr", None))
        self.algo_select.setItemText(5, QCoreApplication.translate("network_ui", u"DyLoRA", None))

#if QT_CONFIG(tooltip)
        self.algo_select.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>The algorithm that is used for training, LoRA is the only one that doesn't train on all layers. LoCon is just LoRA that train on all layers LoHa has a ton of compression, and that is basically true for ia3 and Lokr as well. DyLora is a type of LoRA (or LoCon) that basically allows you to train multiple dim sized models in one, it does take a lot longer to train.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.network_dim_label.setText(QCoreApplication.translate("network_ui", u"Network Dimension", None))
#if QT_CONFIG(tooltip)
        self.network_dim_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>The dimension of the model, the higher the dim the larger the file size. Keep in mind that larger does not mean better. I suggest you keep the dim low.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.network_alpha_label.setText(QCoreApplication.translate("network_ui", u"Network Alpha", None))
#if QT_CONFIG(tooltip)
        self.network_alpha_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>The scalar of the dim. Basically, if you have an alpha of 16 and a dim of 32, then the scalar is 0.5 which is a multiplier on the weights. I suggest you use half dim for alpha, in any case other than less than dim 9, in which I suggest you use alpha 1.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.unet_te_both_label.setText(QCoreApplication.translate("network_ui", u"Train on", None))
        self.unet_te_both_select.setItemText(0, QCoreApplication.translate("network_ui", u"Both", None))
        self.unet_te_both_select.setItemText(1, QCoreApplication.translate("network_ui", u"Unet Only", None))
        self.unet_te_both_select.setItemText(2, QCoreApplication.translate("network_ui", u"Text Encoder Only", None))

#if QT_CONFIG(tooltip)
        self.unet_te_both_select.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>You can train on both the text encoder and unet or only one or the other, most of the time you want to train on both.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.conv_dim_label.setText(QCoreApplication.translate("network_ui", u"Conv Dimension", None))
#if QT_CONFIG(tooltip)
        self.conv_dim_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>The dimension size for the conv layers. These layers carry more style with them, so be careful about setting them too high. I personally suggest you never go higher than 32 with them.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.conv_alpha_label.setText(QCoreApplication.translate("network_ui", u"Conv Alpha", None))
#if QT_CONFIG(tooltip)
        self.conv_alpha_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>The scalar of the conv dims. Much like the normal dim, I suggest you use half conv dim, or 1 if the dim size is 8 or lower.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.dylora_unit_label.setText(QCoreApplication.translate("network_ui", u"DyLoRA Unit", None))
#if QT_CONFIG(tooltip)
        self.dylora_unit_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>The unit is the unit for dividing rank. so if you have dim 16, unit 4, then it can learn 4 lora models of dims 4, 8, 12, and 16.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

