# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_dataset_extra_input.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QFormLayout, QGroupBox,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

from modules.ScrollOnSelect import (DoubleSpinBox, SpinBox)

class Ui_sub_dataset_extra_input(object):
    def setupUi(self, sub_dataset_extra_input):
        if not sub_dataset_extra_input.objectName():
            sub_dataset_extra_input.setObjectName(u"sub_dataset_extra_input")
        sub_dataset_extra_input.resize(488, 358)
        sub_dataset_extra_input.setMinimumSize(QSize(448, 0))
        self.verticalLayout = QVBoxLayout(sub_dataset_extra_input)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.face_crop_group = QGroupBox(sub_dataset_extra_input)
        self.face_crop_group.setObjectName(u"face_crop_group")
        self.face_crop_group.setEnabled(True)
        self.face_crop_group.setCheckable(True)
        self.face_crop_group.setChecked(True)
        self.formLayout_4 = QFormLayout(self.face_crop_group)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.face_crop_width_label = QLabel(self.face_crop_group)
        self.face_crop_width_label.setObjectName(u"face_crop_width_label")
        self.face_crop_width_label.setEnabled(True)

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.face_crop_width_label)

        self.face_crop_width_input = DoubleSpinBox(self.face_crop_group)
        self.face_crop_width_input.setObjectName(u"face_crop_width_input")
        self.face_crop_width_input.setEnabled(True)
        self.face_crop_width_input.setMaximumSize(QSize(16777215, 16777215))
        self.face_crop_width_input.setFocusPolicy(Qt.StrongFocus)
        self.face_crop_width_input.setDecimals(2)
        self.face_crop_width_input.setMinimum(1.000000000000000)
        self.face_crop_width_input.setMaximum(16777215.000000000000000)
        self.face_crop_width_input.setValue(1.000000000000000)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.face_crop_width_input)

        self.face_crop_height_label = QLabel(self.face_crop_group)
        self.face_crop_height_label.setObjectName(u"face_crop_height_label")
        self.face_crop_height_label.setEnabled(True)

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.face_crop_height_label)

        self.face_crop_height_input = DoubleSpinBox(self.face_crop_group)
        self.face_crop_height_input.setObjectName(u"face_crop_height_input")
        self.face_crop_height_input.setEnabled(True)
        self.face_crop_height_input.setFocusPolicy(Qt.StrongFocus)
        self.face_crop_height_input.setDecimals(2)
        self.face_crop_height_input.setMinimum(1.000000000000000)
        self.face_crop_height_input.setMaximum(16777215.000000000000000)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.face_crop_height_input)


        self.verticalLayout.addWidget(self.face_crop_group)

        self.caption_dropout_group = QGroupBox(sub_dataset_extra_input)
        self.caption_dropout_group.setObjectName(u"caption_dropout_group")
        self.caption_dropout_group.setEnabled(True)
        self.caption_dropout_group.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.caption_dropout_group.setCheckable(True)
        self.caption_dropout_group.setChecked(True)
        self.formLayout = QFormLayout(self.caption_dropout_group)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(9, 9, 9, 9)
        self.caption_dropout_rate_label = QLabel(self.caption_dropout_group)
        self.caption_dropout_rate_label.setObjectName(u"caption_dropout_rate_label")
        self.caption_dropout_rate_label.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.caption_dropout_rate_label.sizePolicy().hasHeightForWidth())
        self.caption_dropout_rate_label.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.caption_dropout_rate_label)

        self.caption_dropout_rate_input = DoubleSpinBox(self.caption_dropout_group)
        self.caption_dropout_rate_input.setObjectName(u"caption_dropout_rate_input")
        self.caption_dropout_rate_input.setEnabled(True)
        self.caption_dropout_rate_input.setFocusPolicy(Qt.StrongFocus)
        self.caption_dropout_rate_input.setDecimals(2)
        self.caption_dropout_rate_input.setMinimum(0.000000000000000)
        self.caption_dropout_rate_input.setMaximum(1.000000000000000)
        self.caption_dropout_rate_input.setSingleStep(0.010000000000000)
        self.caption_dropout_rate_input.setStepType(QAbstractSpinBox.DefaultStepType)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.caption_dropout_rate_input)

        self.caption_epoch_dropout_label = QLabel(self.caption_dropout_group)
        self.caption_epoch_dropout_label.setObjectName(u"caption_epoch_dropout_label")
        self.caption_epoch_dropout_label.setEnabled(True)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.caption_epoch_dropout_label)

        self.caption_epoch_dropout_input = SpinBox(self.caption_dropout_group)
        self.caption_epoch_dropout_input.setObjectName(u"caption_epoch_dropout_input")
        self.caption_epoch_dropout_input.setEnabled(True)
        self.caption_epoch_dropout_input.setFocusPolicy(Qt.StrongFocus)
        self.caption_epoch_dropout_input.setMinimum(0)
        self.caption_epoch_dropout_input.setValue(0)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.caption_epoch_dropout_input)

        self.caption_tag_dropout_label = QLabel(self.caption_dropout_group)
        self.caption_tag_dropout_label.setObjectName(u"caption_tag_dropout_label")
        self.caption_tag_dropout_label.setEnabled(True)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.caption_tag_dropout_label)

        self.caption_tag_dropout_input = DoubleSpinBox(self.caption_dropout_group)
        self.caption_tag_dropout_input.setObjectName(u"caption_tag_dropout_input")
        self.caption_tag_dropout_input.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.caption_tag_dropout_input.sizePolicy().hasHeightForWidth())
        self.caption_tag_dropout_input.setSizePolicy(sizePolicy1)
        self.caption_tag_dropout_input.setFocusPolicy(Qt.StrongFocus)
        self.caption_tag_dropout_input.setDecimals(2)
        self.caption_tag_dropout_input.setMinimum(0.000000000000000)
        self.caption_tag_dropout_input.setMaximum(1.000000000000000)
        self.caption_tag_dropout_input.setSingleStep(0.010000000000000)
        self.caption_tag_dropout_input.setStepType(QAbstractSpinBox.DefaultStepType)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.caption_tag_dropout_input)


        self.verticalLayout.addWidget(self.caption_dropout_group)

        self.token_warmup_group = QGroupBox(sub_dataset_extra_input)
        self.token_warmup_group.setObjectName(u"token_warmup_group")
        self.token_warmup_group.setEnabled(True)
        self.token_warmup_group.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.token_warmup_group.setCheckable(True)
        self.token_warmup_group.setChecked(True)
        self.formLayout_3 = QFormLayout(self.token_warmup_group)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.token_minimum_warmup_label = QLabel(self.token_warmup_group)
        self.token_minimum_warmup_label.setObjectName(u"token_minimum_warmup_label")
        self.token_minimum_warmup_label.setEnabled(True)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.token_minimum_warmup_label)

        self.token_minimum_warmup_input = SpinBox(self.token_warmup_group)
        self.token_minimum_warmup_input.setObjectName(u"token_minimum_warmup_input")
        self.token_minimum_warmup_input.setEnabled(True)
        self.token_minimum_warmup_input.setFocusPolicy(Qt.StrongFocus)
        self.token_minimum_warmup_input.setMinimum(1)
        self.token_minimum_warmup_input.setMaximum(255)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.token_minimum_warmup_input)

        self.token_warmup_step_label = QLabel(self.token_warmup_group)
        self.token_warmup_step_label.setObjectName(u"token_warmup_step_label")
        self.token_warmup_step_label.setEnabled(True)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.token_warmup_step_label)

        self.token_warmup_step_input = SpinBox(self.token_warmup_group)
        self.token_warmup_step_input.setObjectName(u"token_warmup_step_input")
        self.token_warmup_step_input.setEnabled(True)
        self.token_warmup_step_input.setFocusPolicy(Qt.StrongFocus)
        self.token_warmup_step_input.setMinimum(1)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.token_warmup_step_input)


        self.verticalLayout.addWidget(self.token_warmup_group)


        self.retranslateUi(sub_dataset_extra_input)

        QMetaObject.connectSlotsByName(sub_dataset_extra_input)
    # setupUi

    def retranslateUi(self, sub_dataset_extra_input):
        sub_dataset_extra_input.setWindowTitle(QCoreApplication.translate("sub_dataset_extra_input", u"Form", None))
#if QT_CONFIG(tooltip)
        self.face_crop_group.setToolTip(QCoreApplication.translate("sub_dataset_extra_input", u"<html><head/><body><p>Suppliments the dataset before training by cropping the face of each image that has one in it. I don't believe this provides extra captions for these files, so this is fairly useless.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.face_crop_group.setTitle(QCoreApplication.translate("sub_dataset_extra_input", u"face crop", None))
        self.face_crop_width_label.setText(QCoreApplication.translate("sub_dataset_extra_input", u"augment range width", None))
#if QT_CONFIG(tooltip)
        self.face_crop_width_input.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.face_crop_height_label.setText(QCoreApplication.translate("sub_dataset_extra_input", u"augment range height", None))
#if QT_CONFIG(tooltip)
        self.caption_dropout_group.setToolTip(QCoreApplication.translate("sub_dataset_extra_input", u"<html><head/><body><p>During training, captions can be excluded according to the various controls below. Personally they don't really serve much of a purpose, I suggest you don't use it.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.caption_dropout_group.setTitle(QCoreApplication.translate("sub_dataset_extra_input", u"caption dropout", None))
        self.caption_dropout_rate_label.setText(QCoreApplication.translate("sub_dataset_extra_input", u"rate", None))
#if QT_CONFIG(tooltip)
        self.caption_dropout_rate_input.setToolTip(QCoreApplication.translate("sub_dataset_extra_input", u"<html><head/><body><p>The default rate that any one caption file gets dropped.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.caption_dropout_rate_input.setPrefix("")
        self.caption_epoch_dropout_label.setText(QCoreApplication.translate("sub_dataset_extra_input", u"rate via epoch", None))
#if QT_CONFIG(tooltip)
        self.caption_epoch_dropout_input.setToolTip(QCoreApplication.translate("sub_dataset_extra_input", u"<html><head/><body><p>This sets how often <span style=\" font-weight:700;\">ALL</span> captions gets dropped. So if you have this set to 1, then <span style=\" font-weight:700;\">ALL</span> captions will be dropped <span style=\" font-weight:700;\">every</span> epoch. If you use this, you should set this higher than 1. Set to 0 to disable.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.caption_tag_dropout_label.setText(QCoreApplication.translate("sub_dataset_extra_input", u"tag dropout rate", None))
#if QT_CONFIG(tooltip)
        self.caption_tag_dropout_input.setToolTip(QCoreApplication.translate("sub_dataset_extra_input", u"<html><head/><body><p>The default rate that any one caption tag gets dropped.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.token_warmup_group.setToolTip(QCoreApplication.translate("sub_dataset_extra_input", u"<html><head/><body><p>Token warmup is a way to gradually introduce tags as the model trains. Both variables are required.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.token_warmup_group.setTitle(QCoreApplication.translate("sub_dataset_extra_input", u"token warmup", None))
        self.token_minimum_warmup_label.setText(QCoreApplication.translate("sub_dataset_extra_input", u"token minimum warmup", None))
#if QT_CONFIG(tooltip)
        self.token_minimum_warmup_input.setToolTip(QCoreApplication.translate("sub_dataset_extra_input", u"<html><head/><body><p>This is the minimum number of tags to be learned at the beginning of the warmup period.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.token_warmup_step_label.setText(QCoreApplication.translate("sub_dataset_extra_input", u"token warmup step", None))
#if QT_CONFIG(tooltip)
        self.token_warmup_step_input.setToolTip(QCoreApplication.translate("sub_dataset_extra_input", u"<html><head/><body><p>The highest step before the warmup is complete. Every step past that uses the full captions.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

