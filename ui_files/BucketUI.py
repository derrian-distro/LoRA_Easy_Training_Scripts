# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BucketUI.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

from modules.ScrollOnSelect import SpinBox

class Ui_bucket_ui(object):
    def setupUi(self, bucket_ui):
        if not bucket_ui.objectName():
            bucket_ui.setObjectName(u"bucket_ui")
        bucket_ui.resize(356, 178)
        self.verticalLayout = QVBoxLayout(bucket_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.bucket_group = QGroupBox(bucket_ui)
        self.bucket_group.setObjectName(u"bucket_group")
        self.bucket_group.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.bucket_group.setCheckable(True)
        self.verticalLayout_2 = QVBoxLayout(self.bucket_group)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.bucket_no_upscale = QCheckBox(self.bucket_group)
        self.bucket_no_upscale.setObjectName(u"bucket_no_upscale")

        self.verticalLayout_2.addWidget(self.bucket_no_upscale, 0, Qt.AlignHCenter)

        self.main_form_layout = QFormLayout()
        self.main_form_layout.setObjectName(u"main_form_layout")
        self.min_label = QLabel(self.bucket_group)
        self.min_label.setObjectName(u"min_label")

        self.main_form_layout.setWidget(0, QFormLayout.LabelRole, self.min_label)

        self.min_input = SpinBox(self.bucket_group)
        self.min_input.setObjectName(u"min_input")
        self.min_input.setFocusPolicy(Qt.StrongFocus)
        self.min_input.setMinimum(0)
        self.min_input.setMaximum(16777215)
        self.min_input.setSingleStep(8)
        self.min_input.setValue(256)

        self.main_form_layout.setWidget(0, QFormLayout.FieldRole, self.min_input)

        self.max_label = QLabel(self.bucket_group)
        self.max_label.setObjectName(u"max_label")

        self.main_form_layout.setWidget(1, QFormLayout.LabelRole, self.max_label)

        self.max_input = SpinBox(self.bucket_group)
        self.max_input.setObjectName(u"max_input")
        self.max_input.setFocusPolicy(Qt.StrongFocus)
        self.max_input.setMinimum(0)
        self.max_input.setMaximum(16777215)
        self.max_input.setSingleStep(8)
        self.max_input.setValue(1024)

        self.main_form_layout.setWidget(1, QFormLayout.FieldRole, self.max_input)

        self.steps_label = QLabel(self.bucket_group)
        self.steps_label.setObjectName(u"steps_label")

        self.main_form_layout.setWidget(2, QFormLayout.LabelRole, self.steps_label)

        self.steps_input = SpinBox(self.bucket_group)
        self.steps_input.setObjectName(u"steps_input")
        self.steps_input.setFocusPolicy(Qt.StrongFocus)
        self.steps_input.setMaximum(16777215)
        self.steps_input.setSingleStep(8)
        self.steps_input.setValue(64)

        self.main_form_layout.setWidget(2, QFormLayout.FieldRole, self.steps_input)


        self.verticalLayout_2.addLayout(self.main_form_layout)


        self.verticalLayout.addWidget(self.bucket_group)


        self.retranslateUi(bucket_ui)

        QMetaObject.connectSlotsByName(bucket_ui)
    # setupUi

    def retranslateUi(self, bucket_ui):
        bucket_ui.setWindowTitle(QCoreApplication.translate("bucket_ui", u"Form", None))
        self.bucket_group.setTitle(QCoreApplication.translate("bucket_ui", u"Enable", None))
#if QT_CONFIG(tooltip)
        self.bucket_no_upscale.setToolTip(QCoreApplication.translate("bucket_ui", u"<html><head/><body><p>Don't Upscale Images doesn't upscale the images provided in the dataset, Additionally, it generates unique buckets to fit the images. This may result in a lot of buckets with only 1 image in them</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.bucket_no_upscale.setText(QCoreApplication.translate("bucket_ui", u"Don't Upscale Images", None))
#if QT_CONFIG(tooltip)
        self.min_label.setToolTip(QCoreApplication.translate("bucket_ui", u"<html><head/><body><p>Minimum Bucket Resolution is the smallest edge of a bucket, this is paired with the Maximum Bucket Resolution to produce the bucket list.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.min_label.setText(QCoreApplication.translate("bucket_ui", u"Minimum Bucket Resolution", None))
#if QT_CONFIG(tooltip)
        self.min_input.setToolTip(QCoreApplication.translate("bucket_ui", u"<html><head/><body><p>Minimum Bucket Resolution is the smallest edge of a bucket, this is paired with the Maximum Bucket Resolution to produce the bucket list.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.max_label.setToolTip(QCoreApplication.translate("bucket_ui", u"<html><head/><body><p>Maximum Bucket Resolution is the largest edge of a bucket, this is paired with the Minimum Bucket Resolution to produce the bucket list.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.max_label.setText(QCoreApplication.translate("bucket_ui", u"Maximum Bucket Resolution", None))
#if QT_CONFIG(tooltip)
        self.max_input.setToolTip(QCoreApplication.translate("bucket_ui", u"<html><head/><body><p>Maximum Bucket Resolution is the largest edge of a bucket, this is paired with the Minimum Bucket Resolution to produce the bucket list.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.steps_label.setToolTip(QCoreApplication.translate("bucket_ui", u"<html><head/><body><p>Bucket Resolution Steps is the amount of pixels between each bucket there is. You don't want this value too large, or too small, as too large would result in images having valuable data being cut off, and too small would cause overlapping and would cause the trainer to crash.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.steps_label.setText(QCoreApplication.translate("bucket_ui", u"Bucket Resolution Steps", None))
#if QT_CONFIG(tooltip)
        self.steps_input.setToolTip(QCoreApplication.translate("bucket_ui", u"<html><head/><body><p>Bucket Resolution Steps is the amount of pixels between each bucket there is. You don't want this value too large, or too small, as too large would result in images having valuable data being cut off, and too small would cause overlapping and would cause the trainer to crash.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

