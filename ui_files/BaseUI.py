# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BaseUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
    QSizePolicy, QTextEdit, QWidget)

from modules.DragDropLineEdit import DragDropLineEdit
from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox)

class Ui_base_args_ui(object):
    def setupUi(self, base_args_ui):
        if not base_args_ui.objectName():
            base_args_ui.setObjectName(u"base_args_ui")
        base_args_ui.resize(553, 518)
        self.gridLayout_3 = QGridLayout(base_args_ui)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.label_7 = QLabel(base_args_ui)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.label_7)

        self.seed_input = SpinBox(base_args_ui)
        self.seed_input.setObjectName(u"seed_input")
        self.seed_input.setFocusPolicy(Qt.StrongFocus)
        self.seed_input.setMinimum(0)
        self.seed_input.setMaximum(16777215)
        self.seed_input.setValue(23)

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.seed_input)

        self.label_9 = QLabel(base_args_ui)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_6.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.clip_skip_input = SpinBox(base_args_ui)
        self.clip_skip_input.setObjectName(u"clip_skip_input")
        self.clip_skip_input.setFocusPolicy(Qt.StrongFocus)
        self.clip_skip_input.setMinimum(1)
        self.clip_skip_input.setValue(2)

        self.formLayout_6.setWidget(1, QFormLayout.FieldRole, self.clip_skip_input)

        self.label_10 = QLabel(base_args_ui)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.label_10)

        self.loss_weight_input = DoubleSpinBox(base_args_ui)
        self.loss_weight_input.setObjectName(u"loss_weight_input")
        self.loss_weight_input.setFocusPolicy(Qt.StrongFocus)
        self.loss_weight_input.setMinimum(0.010000000000000)
        self.loss_weight_input.setSingleStep(0.010000000000000)
        self.loss_weight_input.setValue(1.000000000000000)

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.loss_weight_input)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.cache_latents_enable = QCheckBox(base_args_ui)
        self.cache_latents_enable.setObjectName(u"cache_latents_enable")

        self.horizontalLayout_5.addWidget(self.cache_latents_enable)

        self.cache_latents_to_disk_enable = QCheckBox(base_args_ui)
        self.cache_latents_to_disk_enable.setObjectName(u"cache_latents_to_disk_enable")
        self.cache_latents_to_disk_enable.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.cache_latents_to_disk_enable)


        self.formLayout_6.setLayout(4, QFormLayout.SpanningRole, self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.xformers_enable = QCheckBox(base_args_ui)
        self.xformers_enable.setObjectName(u"xformers_enable")
        self.xformers_enable.setEnabled(True)
        self.xformers_enable.setChecked(False)

        self.horizontalLayout_7.addWidget(self.xformers_enable)

        self.sdpa_enable = QCheckBox(base_args_ui)
        self.sdpa_enable.setObjectName(u"sdpa_enable")

        self.horizontalLayout_7.addWidget(self.sdpa_enable)


        self.formLayout_6.setLayout(3, QFormLayout.SpanningRole, self.horizontalLayout_7)


        self.gridLayout_3.addLayout(self.formLayout_6, 5, 1, 1, 1)

        self.resolution_box = QGroupBox(base_args_ui)
        self.resolution_box.setObjectName(u"resolution_box")
        self.formLayout = QFormLayout(self.resolution_box)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.resolution_box)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.width_input = SpinBox(self.resolution_box)
        self.width_input.setObjectName(u"width_input")
        self.width_input.setFocusPolicy(Qt.StrongFocus)
        self.width_input.setMinimum(1)
        self.width_input.setMaximum(16777215)
        self.width_input.setValue(512)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.width_input)

        self.height_input = SpinBox(self.resolution_box)
        self.height_input.setObjectName(u"height_input")
        self.height_input.setEnabled(False)
        self.height_input.setFocusPolicy(Qt.StrongFocus)
        self.height_input.setMinimum(1)
        self.height_input.setMaximum(16777215)
        self.height_input.setValue(512)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.height_input)

        self.height_enable = QCheckBox(self.resolution_box)
        self.height_enable.setObjectName(u"height_enable")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.height_enable)


        self.gridLayout_3.addWidget(self.resolution_box, 4, 1, 1, 1)

        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_3 = QLabel(base_args_ui)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.batch_size_input = SpinBox(base_args_ui)
        self.batch_size_input.setObjectName(u"batch_size_input")
        self.batch_size_input.setFocusPolicy(Qt.StrongFocus)
        self.batch_size_input.setMinimum(1)

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.batch_size_input)

        self.label_2 = QLabel(base_args_ui)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.max_token_selector = ComboBox(base_args_ui)
        self.max_token_selector.addItem("")
        self.max_token_selector.addItem("")
        self.max_token_selector.addItem("")
        self.max_token_selector.setObjectName(u"max_token_selector")
        self.max_token_selector.setFocusPolicy(Qt.StrongFocus)

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.max_token_selector)

        self.label_5 = QLabel(base_args_ui)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.mixed_precision_selector = ComboBox(base_args_ui)
        self.mixed_precision_selector.addItem("")
        self.mixed_precision_selector.addItem("")
        self.mixed_precision_selector.addItem("")
        self.mixed_precision_selector.setObjectName(u"mixed_precision_selector")
        self.mixed_precision_selector.setFocusPolicy(Qt.StrongFocus)

        self.formLayout_5.setWidget(2, QFormLayout.FieldRole, self.mixed_precision_selector)

        self.label_6 = QLabel(base_args_ui)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.max_train_selector = ComboBox(base_args_ui)
        self.max_train_selector.addItem("")
        self.max_train_selector.addItem("")
        self.max_train_selector.setObjectName(u"max_train_selector")
        self.max_train_selector.setFocusPolicy(Qt.StrongFocus)

        self.horizontalLayout_3.addWidget(self.max_train_selector)

        self.max_train_input = SpinBox(base_args_ui)
        self.max_train_input.setObjectName(u"max_train_input")
        self.max_train_input.setFocusPolicy(Qt.StrongFocus)
        self.max_train_input.setMinimum(1)
        self.max_train_input.setMaximum(16777215)

        self.horizontalLayout_3.addWidget(self.max_train_input)


        self.formLayout_5.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.keep_tokens_seperator_enable = QCheckBox(base_args_ui)
        self.keep_tokens_seperator_enable.setObjectName(u"keep_tokens_seperator_enable")

        self.formLayout_5.setWidget(4, QFormLayout.LabelRole, self.keep_tokens_seperator_enable)

        self.keep_tokens_seperator_input = LineEditWithHighlight(base_args_ui)
        self.keep_tokens_seperator_input.setObjectName(u"keep_tokens_seperator_input")
        self.keep_tokens_seperator_input.setEnabled(False)

        self.formLayout_5.setWidget(4, QFormLayout.FieldRole, self.keep_tokens_seperator_input)


        self.gridLayout_3.addLayout(self.formLayout_5, 5, 2, 1, 1)

        self.groupBox = QGroupBox(base_args_ui)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_8 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.grad_accumulation_enable = QCheckBox(self.groupBox)
        self.grad_accumulation_enable.setObjectName(u"grad_accumulation_enable")

        self.gridLayout.addWidget(self.grad_accumulation_enable, 1, 0, 1, 1)

        self.grad_accumulation_input = SpinBox(self.groupBox)
        self.grad_accumulation_input.setObjectName(u"grad_accumulation_input")
        self.grad_accumulation_input.setEnabled(False)
        self.grad_accumulation_input.setFocusPolicy(Qt.StrongFocus)
        self.grad_accumulation_input.setMinimum(1)

        self.gridLayout.addWidget(self.grad_accumulation_input, 1, 1, 1, 1)

        self.grad_checkpointing_enable = QCheckBox(self.groupBox)
        self.grad_checkpointing_enable.setObjectName(u"grad_checkpointing_enable")

        self.gridLayout.addWidget(self.grad_checkpointing_enable, 0, 0, 1, 2)


        self.horizontalLayout_8.addLayout(self.gridLayout)


        self.gridLayout_3.addWidget(self.groupBox, 4, 2, 1, 1)

        self.base_model_box = QGroupBox(base_args_ui)
        self.base_model_box.setObjectName(u"base_model_box")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.base_model_box.sizePolicy().hasHeightForWidth())
        self.base_model_box.setSizePolicy(sizePolicy)
        self.formLayout_3 = QFormLayout(self.base_model_box)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_4 = QLabel(self.base_model_box)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.base_model_input = DragDropLineEdit(self.base_model_box)
        self.base_model_input.setObjectName(u"base_model_input")

        self.horizontalLayout.addWidget(self.base_model_input)

        self.base_model_selector = QPushButton(self.base_model_box)
        self.base_model_selector.setObjectName(u"base_model_selector")

        self.horizontalLayout.addWidget(self.base_model_selector)


        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.v_param_enable = QCheckBox(self.base_model_box)
        self.v_param_enable.setObjectName(u"v_param_enable")
        self.v_param_enable.setEnabled(True)

        self.horizontalLayout_6.addWidget(self.v_param_enable)

        self.v_pred_enable = QCheckBox(self.base_model_box)
        self.v_pred_enable.setObjectName(u"v_pred_enable")
        self.v_pred_enable.setEnabled(False)

        self.horizontalLayout_6.addWidget(self.v_pred_enable)

        self.FP16_enable = QCheckBox(self.base_model_box)
        self.FP16_enable.setObjectName(u"FP16_enable")

        self.horizontalLayout_6.addWidget(self.FP16_enable)

        self.BF16_enable = QCheckBox(self.base_model_box)
        self.BF16_enable.setObjectName(u"BF16_enable")

        self.horizontalLayout_6.addWidget(self.BF16_enable)

        self.FP8_enable = QCheckBox(self.base_model_box)
        self.FP8_enable.setObjectName(u"FP8_enable")

        self.horizontalLayout_6.addWidget(self.FP8_enable)


        self.formLayout_3.setLayout(3, QFormLayout.SpanningRole, self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.v2_enable = QCheckBox(self.base_model_box)
        self.v2_enable.setObjectName(u"v2_enable")

        self.horizontalLayout_2.addWidget(self.v2_enable)

        self.sdxl_enable = QCheckBox(self.base_model_box)
        self.sdxl_enable.setObjectName(u"sdxl_enable")

        self.horizontalLayout_2.addWidget(self.sdxl_enable)

        self.no_half_vae_enable = QCheckBox(self.base_model_box)
        self.no_half_vae_enable.setObjectName(u"no_half_vae_enable")

        self.horizontalLayout_2.addWidget(self.no_half_vae_enable)

        self.low_ram_enable = QCheckBox(self.base_model_box)
        self.low_ram_enable.setObjectName(u"low_ram_enable")

        self.horizontalLayout_2.addWidget(self.low_ram_enable)


        self.formLayout_3.setLayout(2, QFormLayout.SpanningRole, self.horizontalLayout_2)

        self.label_11 = QLabel(self.base_model_box)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_11)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.vae_input = DragDropLineEdit(self.base_model_box)
        self.vae_input.setObjectName(u"vae_input")

        self.horizontalLayout_4.addWidget(self.vae_input)

        self.vae_selector = QPushButton(self.base_model_box)
        self.vae_selector.setObjectName(u"vae_selector")

        self.horizontalLayout_4.addWidget(self.vae_selector)


        self.formLayout_3.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_4)


        self.gridLayout_3.addWidget(self.base_model_box, 3, 1, 1, 2)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.comment_enable = QCheckBox(base_args_ui)
        self.comment_enable.setObjectName(u"comment_enable")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.comment_enable)

        self.comment_input = QTextEdit(base_args_ui)
        self.comment_input.setObjectName(u"comment_input")
        self.comment_input.setEnabled(False)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.comment_input)


        self.gridLayout_3.addLayout(self.formLayout_2, 6, 1, 1, 2)


        self.retranslateUi(base_args_ui)

        QMetaObject.connectSlotsByName(base_args_ui)
    # setupUi

    def retranslateUi(self, base_args_ui):
        base_args_ui.setWindowTitle(QCoreApplication.translate("base_args_ui", u"Form", None))
        self.label_7.setText(QCoreApplication.translate("base_args_ui", u"Seed", None))
#if QT_CONFIG(tooltip)
        self.seed_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>The seed that is used for the randomization, it also serves as the &quot;reproducable seed&quot; which you can use to see how close it is to the original.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("base_args_ui", u"Clip Skip", None))
#if QT_CONFIG(tooltip)
        self.clip_skip_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>clip skip is how many layers get skipped in training, anime models were trained at clip skip 2 so I suggest you follow that, SD proper was trained at 1.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("base_args_ui", u"Prior Loss Weight", None))
#if QT_CONFIG(tooltip)
        self.loss_weight_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Prior loss weight is a parameter in machine learning that affects how well a model can reproduce images.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.cache_latents_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Caching latents is a way to prevent vram spikes and slightly speed up training time, clashes with color aug, and random crop.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cache_latents_enable.setText(QCoreApplication.translate("base_args_ui", u"Cache Latents", None))
#if QT_CONFIG(tooltip)
        self.cache_latents_to_disk_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Caches the latents to disk, slower, but saves a small bit of vram.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cache_latents_to_disk_enable.setText(QCoreApplication.translate("base_args_ui", u"To Disk", None))
#if QT_CONFIG(tooltip)
        self.xformers_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>A memory optimization, most can use this, AMD and reportedly, some linux devices can't.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.xformers_enable.setText(QCoreApplication.translate("base_args_ui", u"Xformers", None))
        self.sdpa_enable.setText(QCoreApplication.translate("base_args_ui", u"SDPA", None))
        self.resolution_box.setTitle(QCoreApplication.translate("base_args_ui", u"Resolution", None))
        self.label.setText(QCoreApplication.translate("base_args_ui", u"Width", None))
#if QT_CONFIG(tooltip)
        self.width_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Defines the resolution width, or if height isn't selected, both width and height.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.height_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Defines the height of the training resolution, so that you can have non square resolutions.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.height_enable.setText(QCoreApplication.translate("base_args_ui", u"Height", None))
        self.label_3.setText(QCoreApplication.translate("base_args_ui", u"Batch Size", None))
#if QT_CONFIG(tooltip)
        self.batch_size_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>How many images that get processed per step, I usually set this to 2.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("base_args_ui", u"Max Token Length", None))
        self.max_token_selector.setItemText(0, QCoreApplication.translate("base_args_ui", u"225", None))
        self.max_token_selector.setItemText(1, QCoreApplication.translate("base_args_ui", u"150", None))
        self.max_token_selector.setItemText(2, QCoreApplication.translate("base_args_ui", u"75", None))

#if QT_CONFIG(tooltip)
        self.max_token_selector.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>The max token length for captions, or the txt files included in the image folders.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("base_args_ui", u"Training Precision", None))
        self.mixed_precision_selector.setItemText(0, QCoreApplication.translate("base_args_ui", u"fp16", None))
        self.mixed_precision_selector.setItemText(1, QCoreApplication.translate("base_args_ui", u"bf16", None))
        self.mixed_precision_selector.setItemText(2, QCoreApplication.translate("base_args_ui", u"float", None))

#if QT_CONFIG(tooltip)
        self.mixed_precision_selector.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>I suggest bf16 if you have a 30x0 or higher graphics card, but fp16 works as well, float hasn't proven to have a sizable improvement, especially with the extra vram requirement.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("base_args_ui", u"Max Training Time", None))
        self.max_train_selector.setItemText(0, QCoreApplication.translate("base_args_ui", u"Epochs", None))
        self.max_train_selector.setItemText(1, QCoreApplication.translate("base_args_ui", u"Steps", None))

#if QT_CONFIG(tooltip)
        self.max_train_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>This is the maximum amount of steps or epochs, use whichever you find more comfortable using, I personally use steps.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.keep_tokens_seperator_enable.setText(QCoreApplication.translate("base_args_ui", u"Keep Tokens Seperator", None))
        self.groupBox.setTitle(QCoreApplication.translate("base_args_ui", u"Gradient", None))
#if QT_CONFIG(tooltip)
        self.grad_accumulation_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Gradient Accumulation effectively takes your batch size, and then multiplies it by the number listed here. This allows you to simulate having a larger batch size then you have vram, however it is slower.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.grad_accumulation_enable.setText(QCoreApplication.translate("base_args_ui", u"Gradient Accumuation", None))
#if QT_CONFIG(tooltip)
        self.grad_accumulation_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Gradient Accumulation effectively takes your batch size, and then multiplies it by the number listed here. This allows you to simulate having a larger batch size then you have vram, however it is slower.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.grad_checkpointing_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Gradient checkpointing is a trick to reduce vram usage. Do note that this also cuts your performance by about 30% on average</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.grad_checkpointing_enable.setText(QCoreApplication.translate("base_args_ui", u"Gradient Checkpointing", None))
        self.base_model_box.setTitle(QCoreApplication.translate("base_args_ui", u"Model", None))
        self.label_4.setText(QCoreApplication.translate("base_args_ui", u"Base Model", None))
#if QT_CONFIG(tooltip)
        self.base_model_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>The full model to train with, if you are training anime for SD 1.5, I personally suggest NAI.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.base_model_input.setPlaceholderText(QCoreApplication.translate("base_args_ui", u"Base Model To Train With", None))
        self.base_model_selector.setText("")
#if QT_CONFIG(tooltip)
        self.v_param_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Select this if your model uses the SD2.x 768x model, such as WD1.5.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.v_param_enable.setText(QCoreApplication.translate("base_args_ui", u"V Param", None))
        self.v_pred_enable.setText(QCoreApplication.translate("base_args_ui", u"Scale V pred loss", None))
#if QT_CONFIG(tooltip)
        self.FP16_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Allows training on full fp16, not compatable with full bf16 or training precision</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.FP16_enable.setText(QCoreApplication.translate("base_args_ui", u"Full FP16", None))
#if QT_CONFIG(tooltip)
        self.BF16_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Train in full BF16. Requires a higher bitsandbytes than 0.35.0 which is seemingly the best we have on windows, so this is disabled on windows regardless. not compatable with full fp16 or training precision</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.BF16_enable.setText(QCoreApplication.translate("base_args_ui", u"Full BF16", None))
        self.FP8_enable.setText(QCoreApplication.translate("base_args_ui", u"FP8 Base", None))
#if QT_CONFIG(tooltip)
        self.v2_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Select this if you are using an SD2.x based model, such as WD1.5.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.v2_enable.setText(QCoreApplication.translate("base_args_ui", u"SD2.X Based", None))
        self.sdxl_enable.setText(QCoreApplication.translate("base_args_ui", u"SDXL Based", None))
        self.no_half_vae_enable.setText(QCoreApplication.translate("base_args_ui", u"No Half Vae", None))
        self.low_ram_enable.setText(QCoreApplication.translate("base_args_ui", u"Low RAM", None))
        self.label_11.setText(QCoreApplication.translate("base_args_ui", u"External VAE", None))
#if QT_CONFIG(tooltip)
        self.vae_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Allows you to load a vae seperately from the base model.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.vae_input.setPlaceholderText(QCoreApplication.translate("base_args_ui", u"Vae to train with", None))
        self.vae_selector.setText("")
        self.comment_enable.setText(QCoreApplication.translate("base_args_ui", u"Comment", None))
#if QT_CONFIG(tooltip)
        self.comment_input.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Comment that gets put into the metadata</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comment_input.setPlaceholderText(QCoreApplication.translate("base_args_ui", u"Enter in a comment you want in the metadata", None))
    # retranslateUi

