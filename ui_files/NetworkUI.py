# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NetworkUI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

from modules.CollapsibleWidget import CollapsibleWidget
from modules.DragDropLineEdit import DragDropLineEdit
from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox, TabView)

class Ui_network_ui(object):
    def setupUi(self, network_ui):
        if not network_ui.objectName():
            network_ui.setObjectName(u"network_ui")
        network_ui.resize(432, 422)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(network_ui.sizePolicy().hasHeightForWidth())
        network_ui.setSizePolicy(sizePolicy)
        network_ui.setMinimumSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(network_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = TabView(network_ui)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setUsesScrollButtons(False)
        self.main_tab = QWidget()
        self.main_tab.setObjectName(u"main_tab")
        self.main_tab.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gridLayout = QGridLayout(self.main_tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.network_dim_label = QLabel(self.main_tab)
        self.network_dim_label.setObjectName(u"network_dim_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.network_dim_label)

        self.network_dim_input = SpinBox(self.main_tab)
        self.network_dim_input.setObjectName(u"network_dim_input")
        self.network_dim_input.setMaximumSize(QSize(16777215, 16777215))
        self.network_dim_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.network_dim_input.setMinimum(1)
        self.network_dim_input.setMaximum(16777215)
        self.network_dim_input.setValue(32)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.network_dim_input)

        self.network_alpha_label = QLabel(self.main_tab)
        self.network_alpha_label.setObjectName(u"network_alpha_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.network_alpha_label)

        self.network_alpha_input = DoubleSpinBox(self.main_tab)
        self.network_alpha_input.setObjectName(u"network_alpha_input")
        self.network_alpha_input.setMaximumSize(QSize(16777215, 16777215))
        self.network_alpha_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.network_alpha_input.setDecimals(2)
        self.network_alpha_input.setMaximum(16777215.000000000000000)
        self.network_alpha_input.setValue(16.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.network_alpha_input)

        self.min_timestep_label = QLabel(self.main_tab)
        self.min_timestep_label.setObjectName(u"min_timestep_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.min_timestep_label)

        self.min_timestep_input = SpinBox(self.main_tab)
        self.min_timestep_input.setObjectName(u"min_timestep_input")
        self.min_timestep_input.setEnabled(True)
        self.min_timestep_input.setMaximum(999)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.min_timestep_input)


        self.gridLayout.addLayout(self.formLayout, 2, 0, 1, 1)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.network_dropout_enable = QCheckBox(self.main_tab)
        self.network_dropout_enable.setObjectName(u"network_dropout_enable")
        self.network_dropout_enable.setEnabled(True)

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.network_dropout_enable)

        self.network_dropout_input = DoubleSpinBox(self.main_tab)
        self.network_dropout_input.setObjectName(u"network_dropout_input")
        self.network_dropout_input.setEnabled(False)
        self.network_dropout_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.network_dropout_input.setMaximum(1.000000000000000)
        self.network_dropout_input.setSingleStep(0.010000000000000)
        self.network_dropout_input.setValue(0.100000000000000)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.network_dropout_input)

        self.rank_dropout_enable = QCheckBox(self.main_tab)
        self.rank_dropout_enable.setObjectName(u"rank_dropout_enable")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.rank_dropout_enable)

        self.rank_dropout_input = DoubleSpinBox(self.main_tab)
        self.rank_dropout_input.setObjectName(u"rank_dropout_input")
        self.rank_dropout_input.setEnabled(False)
        self.rank_dropout_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.rank_dropout_input.setMaximum(1.000000000000000)
        self.rank_dropout_input.setSingleStep(0.010000000000000)
        self.rank_dropout_input.setValue(0.100000000000000)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.rank_dropout_input)

        self.module_dropout_enable = QCheckBox(self.main_tab)
        self.module_dropout_enable.setObjectName(u"module_dropout_enable")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.module_dropout_enable)

        self.module_dropout_input = DoubleSpinBox(self.main_tab)
        self.module_dropout_input.setObjectName(u"module_dropout_input")
        self.module_dropout_input.setEnabled(False)
        self.module_dropout_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.module_dropout_input.setMaximum(1.000000000000000)
        self.module_dropout_input.setSingleStep(0.010000000000000)
        self.module_dropout_input.setValue(0.100000000000000)

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.module_dropout_input)

        self.lora_fa_enable = QCheckBox(self.main_tab)
        self.lora_fa_enable.setObjectName(u"lora_fa_enable")

        self.formLayout_4.setWidget(4, QFormLayout.SpanningRole, self.lora_fa_enable)

        self.ip_gamma_enable = QCheckBox(self.main_tab)
        self.ip_gamma_enable.setObjectName(u"ip_gamma_enable")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.ip_gamma_enable)

        self.ip_gamma_input = DoubleSpinBox(self.main_tab)
        self.ip_gamma_input.setObjectName(u"ip_gamma_input")
        self.ip_gamma_input.setEnabled(False)
        self.ip_gamma_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.ip_gamma_input.setSingleStep(0.010000000000000)
        self.ip_gamma_input.setValue(0.100000000000000)

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.ip_gamma_input)


        self.gridLayout.addLayout(self.formLayout_4, 4, 1, 1, 1)

        self.lycoris_preset_input = QLineEdit(self.main_tab)
        self.lycoris_preset_input.setObjectName(u"lycoris_preset_input")
        self.lycoris_preset_input.setEnabled(False)

        self.gridLayout.addWidget(self.lycoris_preset_input, 1, 1, 1, 1)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.unet_te_both_label = QLabel(self.main_tab)
        self.unet_te_both_label.setObjectName(u"unet_te_both_label")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.unet_te_both_label)

        self.unet_te_both_select = ComboBox(self.main_tab)
        self.unet_te_both_select.addItem("")
        self.unet_te_both_select.addItem("")
        self.unet_te_both_select.addItem("")
        self.unet_te_both_select.setObjectName(u"unet_te_both_select")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.unet_te_both_select.sizePolicy().hasHeightForWidth())
        self.unet_te_both_select.setSizePolicy(sizePolicy1)
        self.unet_te_both_select.setMinimumSize(QSize(0, 0))
        self.unet_te_both_select.setMaximumSize(QSize(16777215, 16777215))
        self.unet_te_both_select.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.unet_te_both_select)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cache_te_outputs_enable = QCheckBox(self.main_tab)
        self.cache_te_outputs_enable.setObjectName(u"cache_te_outputs_enable")
        self.cache_te_outputs_enable.setEnabled(False)

        self.horizontalLayout.addWidget(self.cache_te_outputs_enable)

        self.cache_te_to_disk_enable = QCheckBox(self.main_tab)
        self.cache_te_to_disk_enable.setObjectName(u"cache_te_to_disk_enable")
        self.cache_te_to_disk_enable.setEnabled(False)

        self.horizontalLayout.addWidget(self.cache_te_to_disk_enable)


        self.formLayout_3.setLayout(1, QFormLayout.SpanningRole, self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cp_enable = QCheckBox(self.main_tab)
        self.cp_enable.setObjectName(u"cp_enable")
        self.cp_enable.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.cp_enable)

        self.train_norm_enable = QCheckBox(self.main_tab)
        self.train_norm_enable.setObjectName(u"train_norm_enable")
        self.train_norm_enable.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.train_norm_enable)

        self.dora_enable = QCheckBox(self.main_tab)
        self.dora_enable.setObjectName(u"dora_enable")
        self.dora_enable.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.dora_enable)


        self.formLayout_3.setLayout(3, QFormLayout.SpanningRole, self.horizontalLayout_3)

        self.rescale_enable = QCheckBox(self.main_tab)
        self.rescale_enable.setObjectName(u"rescale_enable")
        self.rescale_enable.setEnabled(False)

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.rescale_enable)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.dylora_unit_label = QLabel(self.main_tab)
        self.dylora_unit_label.setObjectName(u"dylora_unit_label")
        self.dylora_unit_label.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.dylora_unit_label)

        self.dylora_unit_input = SpinBox(self.main_tab)
        self.dylora_unit_input.setObjectName(u"dylora_unit_input")
        self.dylora_unit_input.setEnabled(False)
        self.dylora_unit_input.setMaximumSize(QSize(16777215, 16777215))
        self.dylora_unit_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.dylora_unit_input.setValue(4)

        self.horizontalLayout_2.addWidget(self.dylora_unit_input)

        self.bypass_mode_enable = QCheckBox(self.main_tab)
        self.bypass_mode_enable.setObjectName(u"bypass_mode_enable")
        self.bypass_mode_enable.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.bypass_mode_enable)


        self.formLayout_3.setLayout(2, QFormLayout.SpanningRole, self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.constrain_enable = QCheckBox(self.main_tab)
        self.constrain_enable.setObjectName(u"constrain_enable")
        self.constrain_enable.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.constrain_enable)

        self.constrain_input = LineEditWithHighlight(self.main_tab)
        self.constrain_input.setObjectName(u"constrain_input")
        self.constrain_input.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.constrain_input)


        self.formLayout_3.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_4)


        self.gridLayout.addLayout(self.formLayout_3, 4, 0, 1, 1)

        self.label = QLabel(self.main_tab)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.conv_dim_label = QLabel(self.main_tab)
        self.conv_dim_label.setObjectName(u"conv_dim_label")
        self.conv_dim_label.setEnabled(True)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.conv_dim_label)

        self.conv_dim_input = SpinBox(self.main_tab)
        self.conv_dim_input.setObjectName(u"conv_dim_input")
        self.conv_dim_input.setEnabled(False)
        self.conv_dim_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.conv_dim_input.setMaximum(16777215)
        self.conv_dim_input.setValue(32)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.conv_dim_input)

        self.conv_alpha_label = QLabel(self.main_tab)
        self.conv_alpha_label.setObjectName(u"conv_alpha_label")
        self.conv_alpha_label.setEnabled(True)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.conv_alpha_label)

        self.conv_alpha_input = DoubleSpinBox(self.main_tab)
        self.conv_alpha_input.setObjectName(u"conv_alpha_input")
        self.conv_alpha_input.setEnabled(False)
        self.conv_alpha_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.conv_alpha_input.setMaximum(16777215.000000000000000)
        self.conv_alpha_input.setValue(16.000000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.conv_alpha_input)

        self.max_timestep_label = QLabel(self.main_tab)
        self.max_timestep_label.setObjectName(u"max_timestep_label")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.max_timestep_label)

        self.max_timestep_input = SpinBox(self.main_tab)
        self.max_timestep_input.setObjectName(u"max_timestep_input")
        self.max_timestep_input.setEnabled(True)
        self.max_timestep_input.setMinimum(1)
        self.max_timestep_input.setMaximum(1000)
        self.max_timestep_input.setValue(1000)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.max_timestep_input)


        self.gridLayout.addLayout(self.formLayout_2, 2, 1, 1, 1)

        self.algo_select = ComboBox(self.main_tab)
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.addItem("")
        self.algo_select.setObjectName(u"algo_select")
        self.algo_select.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.gridLayout.addWidget(self.algo_select, 0, 0, 1, 2)

        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_2 = QLabel(self.main_tab)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.network_weight_file_input = DragDropLineEdit(self.main_tab)
        self.network_weight_file_input.setObjectName(u"network_weight_file_input")

        self.horizontalLayout_6.addWidget(self.network_weight_file_input)

        self.network_weight_file_selector = QPushButton(self.main_tab)
        self.network_weight_file_selector.setObjectName(u"network_weight_file_selector")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.network_weight_file_selector.sizePolicy().hasHeightForWidth())
        self.network_weight_file_selector.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.network_weight_file_selector)


        self.formLayout_5.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_6)

        self.label_3 = QLabel(self.main_tab)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.network_dim_file_input = DragDropLineEdit(self.main_tab)
        self.network_dim_file_input.setObjectName(u"network_dim_file_input")

        self.horizontalLayout_7.addWidget(self.network_dim_file_input)

        self.network_dim_file_selector = QPushButton(self.main_tab)
        self.network_dim_file_selector.setObjectName(u"network_dim_file_selector")
        sizePolicy2.setHeightForWidth(self.network_dim_file_selector.sizePolicy().hasHeightForWidth())
        self.network_dim_file_selector.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.network_dim_file_selector)


        self.formLayout_5.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_7)


        self.gridLayout.addLayout(self.formLayout_5, 5, 0, 1, 2)

        self.tabWidget.addTab(self.main_tab, "")
        self.block_weight_tab = QWidget()
        self.block_weight_tab.setObjectName(u"block_weight_tab")
        self.block_weight_tab.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.verticalLayout_2 = QVBoxLayout(self.block_weight_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.block_weight_scroll_area = QScrollArea(self.block_weight_tab)
        self.block_weight_scroll_area.setObjectName(u"block_weight_scroll_area")
        self.block_weight_scroll_area.setWidgetResizable(True)
        self.block_weight_scroll_widget = QWidget()
        self.block_weight_scroll_widget.setObjectName(u"block_weight_scroll_widget")
        self.block_weight_scroll_widget.setGeometry(QRect(0, 0, 98, 74))
        self.verticalLayout_3 = QVBoxLayout(self.block_weight_scroll_widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.block_weight_widget = CollapsibleWidget(self.block_weight_scroll_widget)
        self.block_weight_widget.setObjectName(u"block_weight_widget")
        self.block_weight_widget.setEnabled(True)

        self.verticalLayout_3.addWidget(self.block_weight_widget)

        self.dim_block_widget = CollapsibleWidget(self.block_weight_scroll_widget)
        self.dim_block_widget.setObjectName(u"dim_block_widget")
        self.dim_block_widget.setEnabled(True)

        self.verticalLayout_3.addWidget(self.dim_block_widget)

        self.alpha_block_widget = CollapsibleWidget(self.block_weight_scroll_widget)
        self.alpha_block_widget.setObjectName(u"alpha_block_widget")
        self.alpha_block_widget.setEnabled(True)

        self.verticalLayout_3.addWidget(self.alpha_block_widget)

        self.conv_block_widget = CollapsibleWidget(self.block_weight_scroll_widget)
        self.conv_block_widget.setObjectName(u"conv_block_widget")
        self.conv_block_widget.setEnabled(False)

        self.verticalLayout_3.addWidget(self.conv_block_widget)

        self.conv_alpha_block_widget = CollapsibleWidget(self.block_weight_scroll_widget)
        self.conv_alpha_block_widget.setObjectName(u"conv_alpha_block_widget")
        self.conv_alpha_block_widget.setEnabled(False)

        self.verticalLayout_3.addWidget(self.conv_alpha_block_widget)

        self.block_weight_scroll_area.setWidget(self.block_weight_scroll_widget)

        self.verticalLayout_2.addWidget(self.block_weight_scroll_area)

        self.tabWidget.addTab(self.block_weight_tab, "")
        self.network_args_tab = QWidget()
        self.network_args_tab.setObjectName(u"network_args_tab")
        self.verticalLayout_4 = QVBoxLayout(self.network_args_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.add_network_arg_button = QPushButton(self.network_args_tab)
        self.add_network_arg_button.setObjectName(u"add_network_arg_button")

        self.horizontalLayout_5.addWidget(self.add_network_arg_button)

        self.save_network_args_button = QPushButton(self.network_args_tab)
        self.save_network_args_button.setObjectName(u"save_network_args_button")
        sizePolicy2.setHeightForWidth(self.save_network_args_button.sizePolicy().hasHeightForWidth())
        self.save_network_args_button.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.save_network_args_button)

        self.load_network_args_button = QPushButton(self.network_args_tab)
        self.load_network_args_button.setObjectName(u"load_network_args_button")
        sizePolicy2.setHeightForWidth(self.load_network_args_button.sizePolicy().hasHeightForWidth())
        self.load_network_args_button.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.load_network_args_button)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.scrollArea = QScrollArea(self.network_args_tab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.network_args_item_widget = QWidget()
        self.network_args_item_widget.setObjectName(u"network_args_item_widget")
        self.network_args_item_widget.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_5 = QVBoxLayout(self.network_args_item_widget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.scrollArea.setWidget(self.network_args_item_widget)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.network_args_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(network_ui)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(network_ui)
    # setupUi

    def retranslateUi(self, network_ui):
        network_ui.setWindowTitle(QCoreApplication.translate("network_ui", u"Form", None))
#if QT_CONFIG(tooltip)
        self.network_dim_label.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Network Dimension represents the size of the Linear Dimensions of the model</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.network_dim_label.setText(QCoreApplication.translate("network_ui", u"Network Dimension", None))
#if QT_CONFIG(tooltip)
        self.network_dim_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Network Dimension represents the size of the Linear Dimensions of the model</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.network_alpha_label.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Network Alpha represents the alpha of the Linear Dimensions. This Alpha is a scalar on the network dimension such that alpha / dimension = scalar. For example, and alpha of 16 and a dimension of 32 would result in a scalar of 0.5</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.network_alpha_label.setText(QCoreApplication.translate("network_ui", u"Network Alpha", None))
#if QT_CONFIG(tooltip)
        self.network_alpha_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Network Alpha represents the alpha of the Linear Dimensions. This Alpha is a scalar on the network dimension such that alpha / dimension = scalar. For example, and alpha of 16 and a dimension of 32 would result in a scalar of 0.5</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.min_timestep_label.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Min timestep represents the lowest timestep to train on. Typically you want to keep this value at 0</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.min_timestep_label.setText(QCoreApplication.translate("network_ui", u"Min Timestep", None))
#if QT_CONFIG(tooltip)
        self.min_timestep_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Min timestep represents the lowest timestep to train on. Typically you want to keep this value at 0</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.network_dropout_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Network Dropout, otherwise known as Neuron Dropout is your standard dropout provided by PyTorch.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.network_dropout_enable.setText(QCoreApplication.translate("network_ui", u"Network Dropout", None))
#if QT_CONFIG(tooltip)
        self.network_dropout_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Network Dropout, otherwise known as Neuron Dropout is your standard dropout provided by PyTorch.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.rank_dropout_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Rank Dropout is a larger form of dropout, randomly dropping out a full rank</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.rank_dropout_enable.setText(QCoreApplication.translate("network_ui", u"Rank Dropout", None))
#if QT_CONFIG(tooltip)
        self.rank_dropout_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Rank Dropout is a larger form of dropout, randomly dropping out a full rank</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.module_dropout_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Module Dropout is a larger form of dropout, randomly dropping out a full module</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.module_dropout_enable.setText(QCoreApplication.translate("network_ui", u"Module Dropout", None))
#if QT_CONFIG(tooltip)
        self.module_dropout_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Module Dropout is a larger form of dropout, randomly dropping out a full module</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lora_fa_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>LoRA FA is a tweak to the LoRA algorithm that is supposed to reduce the VRAM requirement while keeping all else the same</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lora_fa_enable.setText(QCoreApplication.translate("network_ui", u"LoRA FA", None))
#if QT_CONFIG(tooltip)
        self.ip_gamma_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>IP Noise Gamma is a noise modification that reduces the random noise, allowing what you want to learn, to learn faster</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ip_gamma_enable.setText(QCoreApplication.translate("network_ui", u"IP Noise Gamma", None))
#if QT_CONFIG(tooltip)
        self.ip_gamma_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>IP Noise Gamma is a noise modification that reduces the random noise, allowing what you want to learn, to learn faster</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lycoris_preset_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>LyCORIS Preset is the preset used by the LyCORIS library. Typically you want to use &quot;full&quot; which is automatically selected when there is nothing provided</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.unet_te_both_label.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Train on selects if you want to train Both the Text Encoder and the Unet, only the Text Encoder, or only the Unet.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.unet_te_both_label.setText(QCoreApplication.translate("network_ui", u"Train on", None))
        self.unet_te_both_select.setItemText(0, QCoreApplication.translate("network_ui", u"Both", None))
        self.unet_te_both_select.setItemText(1, QCoreApplication.translate("network_ui", u"Unet Only", None))
        self.unet_te_both_select.setItemText(2, QCoreApplication.translate("network_ui", u"TE Only", None))

#if QT_CONFIG(tooltip)
        self.unet_te_both_select.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Train on selects if you want to train Both the Text Encoder and the Unet, only the Text Encoder, or only the Unet.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.cache_te_outputs_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Cache TE Outputs caches the Text encoder outputs, which reduces the vram requirement. This does, however, prevent you from training the Text Encoder</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cache_te_outputs_enable.setText(QCoreApplication.translate("network_ui", u"Cache TE Outputs", None))
#if QT_CONFIG(tooltip)
        self.cache_te_to_disk_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Caches the Text Encoder outputs to disk, which allows for reuse if you provide the same dataset</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cache_te_to_disk_enable.setText(QCoreApplication.translate("network_ui", u"To Disk", None))
#if QT_CONFIG(tooltip)
        self.cp_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Tucker, is a form of compression algorithm that reduces the file size</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cp_enable.setText(QCoreApplication.translate("network_ui", u"Tucker", None))
#if QT_CONFIG(tooltip)
        self.train_norm_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Train Norm allows the model to train the Normalization Layers</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.train_norm_enable.setText(QCoreApplication.translate("network_ui", u"Train Norm", None))
#if QT_CONFIG(tooltip)
        self.dora_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>DoRA activates Weight Decomoposition</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.dora_enable.setText(QCoreApplication.translate("network_ui", u"DoRA", None))
#if QT_CONFIG(tooltip)
        self.rescale_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Rescaled rescales the weights. Specific to Diag-OFT</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.rescale_enable.setText(QCoreApplication.translate("network_ui", u"Rescaled", None))
#if QT_CONFIG(tooltip)
        self.dylora_unit_label.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>DyLoRA Unit is the number to jump by per DyLoRA layer.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.dylora_unit_label.setText(QCoreApplication.translate("network_ui", u"DyLoRA Unit", None))
#if QT_CONFIG(tooltip)
        self.dylora_unit_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>DyLoRA Unit is the number to jump by per DyLoRA layer.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.bypass_mode_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Bypass mode changes the calculations in some way</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.bypass_mode_enable.setText(QCoreApplication.translate("network_ui", u"Bypass Mode", None))
#if QT_CONFIG(tooltip)
        self.constrain_enable.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Constrait constrains the weights. Specific to Diag-OFT</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.constrain_enable.setText(QCoreApplication.translate("network_ui", u"Constraint", None))
#if QT_CONFIG(tooltip)
        self.constrain_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Constrait constrains the weights. Specific to Diag-OFT</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>LyCORIS Preset is the preset used by the LyCORIS library. Typically you want to use &quot;full&quot; which is automatically selected when there is nothing provided</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("network_ui", u"LyCORIS Preset", None))
#if QT_CONFIG(tooltip)
        self.conv_dim_label.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Conv Dimension represents the size of the Convolutional Dimensions of the model</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.conv_dim_label.setText(QCoreApplication.translate("network_ui", u"Conv Dimension", None))
#if QT_CONFIG(tooltip)
        self.conv_dim_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Conv Dimension represents the size of the Convolutional Dimensions of the model</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.conv_alpha_label.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Conv Alpha represents the alpha of the Conv Dimensions. This Alpha is a scalar on the conv dimension such that alpha / dimension = scalar. For example, and alpha of 16 and a dimension of 32 would result in a scalar of 0.5</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.conv_alpha_label.setText(QCoreApplication.translate("network_ui", u"Conv Alpha", None))
#if QT_CONFIG(tooltip)
        self.conv_alpha_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Conv Alpha represents the alpha of the Conv Dimensions. This Alpha is a scalar on the conv dimension such that alpha / dimension = scalar. For example, and alpha of 16 and a dimension of 32 would result in a scalar of 0.5</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.max_timestep_label.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Max Timestep represents the lowest timestep to train on. Typically you want to keep this value at 1000, the highest possible timestep. The Max timestep cannot be lower than the Min Timestep</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.max_timestep_label.setText(QCoreApplication.translate("network_ui", u"Max Timestep", None))
#if QT_CONFIG(tooltip)
        self.max_timestep_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Max Timestep represents the lowest timestep to train on. Typically you want to keep this value at 1000, the highest possible timestep. The Max timestep cannot be lower than the Min Timestep</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.algo_select.setItemText(0, QCoreApplication.translate("network_ui", u"LoRA", None))
        self.algo_select.setItemText(1, QCoreApplication.translate("network_ui", u"LoCon", None))
        self.algo_select.setItemText(2, QCoreApplication.translate("network_ui", u"LoCon (LyCORIS)", None))
        self.algo_select.setItemText(3, QCoreApplication.translate("network_ui", u"LoHa", None))
        self.algo_select.setItemText(4, QCoreApplication.translate("network_ui", u"IA3", None))
        self.algo_select.setItemText(5, QCoreApplication.translate("network_ui", u"Lokr", None))
        self.algo_select.setItemText(6, QCoreApplication.translate("network_ui", u"DyLoRA", None))
        self.algo_select.setItemText(7, QCoreApplication.translate("network_ui", u"BOFT", None))
        self.algo_select.setItemText(8, QCoreApplication.translate("network_ui", u"Diag-OFT", None))
        self.algo_select.setItemText(9, QCoreApplication.translate("network_ui", u"Full", None))

#if QT_CONFIG(tooltip)
        self.algo_select.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>The Algorithm that is used during training</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Use an existing LoRA to apply to the base model as weights, effectively allowing you to begin training from a previous epoch, or LoRA</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("network_ui", u"Weights From Network", None))
#if QT_CONFIG(tooltip)
        self.network_weight_file_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Use an existing LoRA to apply to the base model as weights, effectively allowing you to begin training from a previous epoch, or LoRA</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.network_weight_file_selector.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Use an existing LoRA to apply to the base model as weights, effectively allowing you to begin training from a previous epoch, or LoRA</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.network_weight_file_selector.setText("")
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Use an existing LoRA to select the dims for this new LoRA. This method of selecting dims allows for more dynamic dims, similar to using the block weights</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("network_ui", u"Dims From Network", None))
#if QT_CONFIG(tooltip)
        self.network_dim_file_input.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Use an existing LoRA to select the dims for this new LoRA. This method of selecting dims allows for more dynamic dims, similar to using the block weights</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.network_dim_file_selector.setToolTip(QCoreApplication.translate("network_ui", u"<html><head/><body><p>Use an existing LoRA to select the dims for this new LoRA. This method of selecting dims allows for more dynamic dims, similar to using the block weights</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.network_dim_file_selector.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main_tab), QCoreApplication.translate("network_ui", u"Main Args", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.block_weight_tab), QCoreApplication.translate("network_ui", u"Block Weights", None))
        self.add_network_arg_button.setText(QCoreApplication.translate("network_ui", u"Add Network Arg", None))
        self.save_network_args_button.setText("")
        self.load_network_args_button.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.network_args_tab), QCoreApplication.translate("network_ui", u"Network Args", None))
    # retranslateUi

