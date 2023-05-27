# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoggingUI.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

from modules.DragDropLineEdit import DragDropLineEdit
from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import ComboBox

class Ui_logging_ui(object):
    def setupUi(self, logging_ui):
        if not logging_ui.objectName():
            logging_ui.setObjectName(u"logging_ui")
        logging_ui.resize(440, 207)
        logging_ui.setMinimumSize(QSize(440, 0))
        self.verticalLayout = QVBoxLayout(logging_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logging_group = QGroupBox(logging_ui)
        self.logging_group.setObjectName(u"logging_group")
        self.logging_group.setCheckable(True)
        self.logging_group.setChecked(False)
        self.formLayout = QFormLayout(self.logging_group)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.logging_group)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.log_output_input = DragDropLineEdit(self.logging_group)
        self.log_output_input.setObjectName(u"log_output_input")

        self.horizontalLayout.addWidget(self.log_output_input)

        self.log_output_selector = QPushButton(self.logging_group)
        self.log_output_selector.setObjectName(u"log_output_selector")

        self.horizontalLayout.addWidget(self.log_output_selector)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_2 = QLabel(self.logging_group)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.log_mode_selector = ComboBox(self.logging_group)
        self.log_mode_selector.addItem("")
        self.log_mode_selector.addItem("")
        self.log_mode_selector.addItem("")
        self.log_mode_selector.setObjectName(u"log_mode_selector")
        self.log_mode_selector.setFocusPolicy(Qt.StrongFocus)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.log_mode_selector)

        self.log_prefix_input = LineEditWithHighlight(self.logging_group)
        self.log_prefix_input.setObjectName(u"log_prefix_input")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.log_prefix_input)

        self.log_tracker_name_input = LineEditWithHighlight(self.logging_group)
        self.log_tracker_name_input.setObjectName(u"log_tracker_name_input")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.log_tracker_name_input)

        self.label_5 = QLabel(self.logging_group)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.log_wandb_key_input = LineEditWithHighlight(self.logging_group)
        self.log_wandb_key_input.setObjectName(u"log_wandb_key_input")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.log_wandb_key_input)

        self.log_prefix_enable = QCheckBox(self.logging_group)
        self.log_prefix_enable.setObjectName(u"log_prefix_enable")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.log_prefix_enable)

        self.log_tracker_name_enable = QCheckBox(self.logging_group)
        self.log_tracker_name_enable.setObjectName(u"log_tracker_name_enable")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.log_tracker_name_enable)


        self.verticalLayout.addWidget(self.logging_group)


        self.retranslateUi(logging_ui)

        QMetaObject.connectSlotsByName(logging_ui)
    # setupUi

    def retranslateUi(self, logging_ui):
        logging_ui.setWindowTitle(QCoreApplication.translate("logging_ui", u"Form", None))
        self.logging_group.setTitle(QCoreApplication.translate("logging_ui", u"Enable", None))
        self.label.setText(QCoreApplication.translate("logging_ui", u"Log Output Directory", None))
#if QT_CONFIG(tooltip)
        self.log_output_input.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>The folder that the log folders will be output to.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_output_input.setPlaceholderText(QCoreApplication.translate("logging_ui", u"Output Directory", None))
        self.log_output_selector.setText("")
        self.label_2.setText(QCoreApplication.translate("logging_ui", u"Logging System", None))
        self.log_mode_selector.setItemText(0, QCoreApplication.translate("logging_ui", u"Tensorboard", None))
        self.log_mode_selector.setItemText(1, QCoreApplication.translate("logging_ui", u"Wandb", None))
        self.log_mode_selector.setItemText(2, QCoreApplication.translate("logging_ui", u"All", None))

#if QT_CONFIG(tooltip)
        self.log_mode_selector.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>The system you use for logging. Tensorboard is local, Wandb is cloud based. You can also opt to log in both of them.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.log_prefix_input.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>This is the name that gets added to the front of the folder name so that you can tell what log is what.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_prefix_input.setPlaceholderText(QCoreApplication.translate("logging_ui", u"Prefix", None))
#if QT_CONFIG(tooltip)
        self.log_tracker_name_input.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Is the name of the tracker in the logged data.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_tracker_name_input.setPlaceholderText(QCoreApplication.translate("logging_ui", u"Tracker Name", None))
        self.label_5.setText(QCoreApplication.translate("logging_ui", u"Wandb API Key", None))
#if QT_CONFIG(tooltip)
        self.log_wandb_key_input.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Required if you are using Wandb as it's how you connect to the service.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_wandb_key_input.setPlaceholderText(QCoreApplication.translate("logging_ui", u"API Key", None))
        self.log_prefix_enable.setText(QCoreApplication.translate("logging_ui", u"Prefix For Log Folders", None))
        self.log_tracker_name_enable.setText(QCoreApplication.translate("logging_ui", u"Name For Log Tracker", None))
    # retranslateUi

