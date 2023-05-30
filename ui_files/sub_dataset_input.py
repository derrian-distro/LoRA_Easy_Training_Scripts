# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_dataset_input.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGridLayout,
    QLabel, QLayout, QPushButton, QSizePolicy,
    QWidget)

from modules.CollapsibleWidget import CollapsibleWidget
from modules.DragDropLineEdit import DragDropLineEdit
from modules.ScrollOnSelect import (ComboBox, SpinBox)

class Ui_sub_dataset_input(object):
    def setupUi(self, sub_dataset_input):
        if not sub_dataset_input.objectName():
            sub_dataset_input.setObjectName(u"sub_dataset_input")
        sub_dataset_input.resize(523, 167)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(sub_dataset_input.sizePolicy().hasHeightForWidth())
        sub_dataset_input.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(sub_dataset_input)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 9, 9, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.flip_aug = QCheckBox(sub_dataset_input)
        self.flip_aug.setObjectName(u"flip_aug")

        self.gridLayout_2.addWidget(self.flip_aug, 0, 1, 1, 1, Qt.AlignLeft)

        self.shuffle_captions = QCheckBox(sub_dataset_input)
        self.shuffle_captions.setObjectName(u"shuffle_captions")

        self.gridLayout_2.addWidget(self.shuffle_captions, 0, 0, 1, 1, Qt.AlignLeft)

        self.random_crop = QCheckBox(sub_dataset_input)
        self.random_crop.setObjectName(u"random_crop")

        self.gridLayout_2.addWidget(self.random_crop, 1, 1, 1, 1, Qt.AlignLeft)

        self.color_aug = QCheckBox(sub_dataset_input)
        self.color_aug.setObjectName(u"color_aug")

        self.gridLayout_2.addWidget(self.color_aug, 1, 0, 1, 1, Qt.AlignLeft)

        self.reg_images = QCheckBox(sub_dataset_input)
        self.reg_images.setObjectName(u"reg_images")

        self.gridLayout_2.addWidget(self.reg_images, 2, 0, 1, 2, Qt.AlignLeft)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 1, 1, 1)

        self.other_form_layout = QFormLayout()
        self.other_form_layout.setObjectName(u"other_form_layout")
        self.other_form_layout.setHorizontalSpacing(12)
        self.repeats_label = QLabel(sub_dataset_input)
        self.repeats_label.setObjectName(u"repeats_label")

        self.other_form_layout.setWidget(0, QFormLayout.LabelRole, self.repeats_label)

        self.repeats_spinbox = SpinBox(sub_dataset_input)
        self.repeats_spinbox.setObjectName(u"repeats_spinbox")
        self.repeats_spinbox.setMaximumSize(QSize(16777215, 16777215))
        self.repeats_spinbox.setFocusPolicy(Qt.StrongFocus)
        self.repeats_spinbox.setMinimum(1)
        self.repeats_spinbox.setMaximum(16777215)

        self.other_form_layout.setWidget(0, QFormLayout.FieldRole, self.repeats_spinbox)

        self.keep_tokens_label = QLabel(sub_dataset_input)
        self.keep_tokens_label.setObjectName(u"keep_tokens_label")

        self.other_form_layout.setWidget(1, QFormLayout.LabelRole, self.keep_tokens_label)

        self.keep_tokens_spinbox = SpinBox(sub_dataset_input)
        self.keep_tokens_spinbox.setObjectName(u"keep_tokens_spinbox")
        self.keep_tokens_spinbox.setFocusPolicy(Qt.StrongFocus)

        self.other_form_layout.setWidget(1, QFormLayout.FieldRole, self.keep_tokens_spinbox)

        self.caption_label = QLabel(sub_dataset_input)
        self.caption_label.setObjectName(u"caption_label")

        self.other_form_layout.setWidget(2, QFormLayout.LabelRole, self.caption_label)

        self.caption_extension = ComboBox(sub_dataset_input)
        self.caption_extension.addItem("")
        self.caption_extension.addItem("")
        self.caption_extension.setObjectName(u"caption_extension")
        self.caption_extension.setFocusPolicy(Qt.StrongFocus)

        self.other_form_layout.setWidget(2, QFormLayout.FieldRole, self.caption_extension)


        self.gridLayout.addLayout(self.other_form_layout, 1, 0, 1, 1)

        self.image_dir_grid = QGridLayout()
        self.image_dir_grid.setObjectName(u"image_dir_grid")
        self.image_dir_grid.setHorizontalSpacing(8)
        self.file_dialog_button = QPushButton(sub_dataset_input)
        self.file_dialog_button.setObjectName(u"file_dialog_button")

        self.image_dir_grid.addWidget(self.file_dialog_button, 1, 1, 1, 1)

        self.Input_image_dir_label = QLabel(sub_dataset_input)
        self.Input_image_dir_label.setObjectName(u"Input_image_dir_label")

        self.image_dir_grid.addWidget(self.Input_image_dir_label, 0, 0, 1, 2)

        self.lineEdit = DragDropLineEdit(sub_dataset_input)
        self.lineEdit.setObjectName(u"lineEdit")

        self.image_dir_grid.addWidget(self.lineEdit, 1, 0, 1, 1)


        self.gridLayout.addLayout(self.image_dir_grid, 0, 0, 1, 2)

        self.extra_args = CollapsibleWidget(sub_dataset_input)
        self.extra_args.setObjectName(u"extra_args")

        self.gridLayout.addWidget(self.extra_args, 3, 0, 1, 2)


        self.retranslateUi(sub_dataset_input)

        QMetaObject.connectSlotsByName(sub_dataset_input)
    # setupUi

    def retranslateUi(self, sub_dataset_input):
        sub_dataset_input.setWindowTitle(QCoreApplication.translate("sub_dataset_input", u"Widget", None))
#if QT_CONFIG(tooltip)
        self.flip_aug.setToolTip(QCoreApplication.translate("sub_dataset_input", u"<html><head/><body><p>Flips the latents of the images during training. Works well to reduce bias according to sidedness, but can cause issues if the dataset is asymetric.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.flip_aug.setText(QCoreApplication.translate("sub_dataset_input", u"flip augment", None))
#if QT_CONFIG(tooltip)
        self.shuffle_captions.setToolTip(QCoreApplication.translate("sub_dataset_input", u"<html><head/><body><p>During training, the captions in the caption files will be shuffed. If you set keep tokens any higher than 0, then tags equal to keep tokens will not be shuffled and stay at the front, great for keeping something like a character name at the front of the file. I suggest you turn this on as it reduces overfitting.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.shuffle_captions.setText(QCoreApplication.translate("sub_dataset_input", u"shuffle captions", None))
#if QT_CONFIG(tooltip)
        self.random_crop.setToolTip(QCoreApplication.translate("sub_dataset_input", u"<html><head/><body><p>Randomly crops from a corner vs from the center. Works very well when you have parts of the images that you want to learn that are on the edges. Doesn't work with cache latents.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.random_crop.setText(QCoreApplication.translate("sub_dataset_input", u"random crop", None))
#if QT_CONFIG(tooltip)
        self.color_aug.setToolTip(QCoreApplication.translate("sub_dataset_input", u"<html><head/><body><p>Shifts the color of images randomly throughout training. This doesn't change captions however so it's fairly useless. Doesn't work with cache latents.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.color_aug.setText(QCoreApplication.translate("sub_dataset_input", u"color augment", None))
#if QT_CONFIG(tooltip)
        self.reg_images.setToolTip(QCoreApplication.translate("sub_dataset_input", u"<html><head/><body><p>Select this if the folder provided is to images that are regularization images.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.reg_images.setText(QCoreApplication.translate("sub_dataset_input", u"regularization images", None))
        self.repeats_label.setText(QCoreApplication.translate("sub_dataset_input", u"Number of Repeats", None))
#if QT_CONFIG(tooltip)
        self.repeats_spinbox.setToolTip(QCoreApplication.translate("sub_dataset_input", u"<html><head/><body><p>This is the number of times the images in this folder will repeat per epoch. So if you have 30 images in this folder and 4 repeats, it will be treated like as if it has 120 images.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.keep_tokens_label.setText(QCoreApplication.translate("sub_dataset_input", u"Keep Tokens", None))
#if QT_CONFIG(tooltip)
        self.keep_tokens_spinbox.setToolTip(QCoreApplication.translate("sub_dataset_input", u"<html><head/><body><p>This is the number of tokens that get kept at the front of the captions. This is great when you want to have a tag that is always weighted the highest, such as the name of a character or an outfit tag.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.caption_label.setText(QCoreApplication.translate("sub_dataset_input", u"Caption Extension", None))
        self.caption_extension.setItemText(0, QCoreApplication.translate("sub_dataset_input", u".txt", None))
        self.caption_extension.setItemText(1, QCoreApplication.translate("sub_dataset_input", u".caption", None))

#if QT_CONFIG(tooltip)
        self.caption_extension.setToolTip(QCoreApplication.translate("sub_dataset_input", u"<html><head/><body><p>The file type of the captions, technically can be anything but I only included the two most common types, .caption, and .txt.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.file_dialog_button.setText("")
        self.Input_image_dir_label.setText(QCoreApplication.translate("sub_dataset_input", u"Input Image Dir", None))
#if QT_CONFIG(tooltip)
        self.lineEdit.setToolTip(QCoreApplication.translate("sub_dataset_input", u"<html><head/><body><p>The folder that contains your images and caption files. If the folder is named something like 2_name, then it will automatically set the number of repeats, but only if you use the file dialog or drag and drop.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("sub_dataset_input", u"Image Dir", None))
    # retranslateUi

